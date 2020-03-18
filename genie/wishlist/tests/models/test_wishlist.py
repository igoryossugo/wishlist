from decimal import Decimal

import pytest
from asynctest import mock
from simple_settings import settings

from genie.contrib.caches import Cache
from genie.customer.models import CustomerModel
from genie.wishlist.exceptions import WishlistAlreadyExistsForCustomer
from genie.wishlist.models.item import ItemModel
from genie.wishlist.models.wishlist import Wishlist, WishlistModel


class TestWishlistModel:

    def test_get_calls_item_model(self):
        with mock.patch(
            'genie.wishlist.models.wishlist.ItemModel.get'
        ) as mocked_item:
            WishlistModel.get(id='a')

        mocked_item.assert_called_with(wishlist_id='a')

    def test_from_dict_returns_model_instance(self):
        wishlist = WishlistModel.from_dict(data={'id': 'a'})
        assert isinstance(wishlist, WishlistModel)
        assert wishlist.id == 'a'

    def test_add_item_should_increment_items(self, item_model):
        wishlist = WishlistModel(id='a')
        assert wishlist.items is None

        wishlist.add_item(item_model)
        assert wishlist.items == [item_model]

        wishlist.add_item(item_model)
        assert wishlist.items == [item_model, item_model]

    def test_remove_item_should_decrement_items(self, item_model):
        item_model_a = item_model
        item_model_b = ItemModel(
            sku='82727b28-d6b3-813c-5139-50d3b28c16d4-b',
            title='Alcool em gel',
            image_url=(
                'http://challenge-api.luizalabs.com/images/'
                '82727b28-d6b3-813c-5139-50d3b28c16d4.jpg'
            ),
            price=Decimal('34.9'),
            brand='epoch magia',
            review_score=4.3
        )
        wishlist = WishlistModel(id='a', items=[item_model_a, item_model_b])
        wishlist.remove_item(sku=item_model_a.sku)
        assert wishlist.items == [item_model_b]

    def test_save_calls_item_save_and_base_save(self, item_model):
        wishlist = WishlistModel(id='a', items=[item_model])
        with mock.patch(
            'genie.wishlist.models.wishlist.BaseModel.save'
        ) as mocked_save:
            with mock.patch.object(item_model, 'save') as mocked_item_save:
                wishlist.save()

        assert mocked_save.called
        assert mocked_item_save.called


class TestWishlist:

    @pytest.fixture
    def model_customer(self):
        return CustomerModel(
            id='a',
            name='igor',
            email='test@test.com',
        )

    @pytest.fixture
    def mocked_customer_model(self):
        return mock.patch('genie.wishlist.models.wishlist.CustomerModel.get')

    @pytest.fixture
    def mocked_catalog_backend(self, item):
        return mock.patch(
            'genie.extensions.fake.backends.catalog.'
            'FakeSuccessCatalogBackend.get_item',
            return_value=item
        )

    def test_create_calls_customer_models_get(
        self,
        mocked_customer_model,
        model_customer
    ):
        with mocked_customer_model as mocked_customer:
            mocked_customer.return_value = model_customer
            Wishlist.create(customer_id='a')

        mocked_customer.assert_called_with(customer_id='a')

    def test_create_returns_instance_with_default_attributes(
        self,
        mocked_customer_model,
        model_customer
    ):
        with mocked_customer_model as mocked_customer:
            mocked_customer.return_value = model_customer
            wishlist = Wishlist.create(customer_id='a')

        assert isinstance(wishlist, Wishlist)
        assert isinstance(wishlist.model, WishlistModel)
        assert isinstance(wishlist._cache, Cache)

    def test_create_raises_exception_when_customer_has_wishlist_id(
        self,
        mocked_customer_model,
        model_customer
    ):
        with mocked_customer_model as mocked_customer:
            model_customer.wishlist_id = 'a'
            mocked_customer.return_value = model_customer
            with pytest.raises(WishlistAlreadyExistsForCustomer):
                    Wishlist.create(customer_id='a')

    async def test_save_calls_cache_and_model(self):
        wishlist = Wishlist(wishlist_id='a')
        with mock.patch.object(Cache, 'set') as mocked_cache:
            with mock.patch.object(wishlist, 'model') as mocked_model:
                await wishlist.save()

        mocked_cache.assert_called_with(
            mocked_model.id,
            mocked_model.to_dict(),
            settings.WISHLIST_CACHE_MAX_AGE
        )
        assert mocked_model.save.called

    async def test_add_item_calls_catalog_and_model(
        self,
        mocked_catalog_backend,
    ):
        wishlist = Wishlist('a')
        with mocked_catalog_backend as mocked_catalog:
            with mock.patch.object(wishlist, 'model') as mocked_model:
                with mock.patch.object(wishlist, 'save') as mocked_save:
                    await wishlist.add_item(sku='abc')

        mocked_catalog.assert_called_with(sku='abc'),
        assert mocked_model.add_item.called
        assert mocked_save.called

    async def test_remove_item_calls_model(self):
        wishlist = Wishlist('a')
        with mock.patch.object(wishlist.model, 'remove_item') as mocked_model:
            with mock.patch.object(wishlist, 'save') as mocked_save:
                await wishlist.remove_item(sku='b')

        mocked_model.assert_called_with(sku='b')
        assert mocked_save.called

    async def test_get_calls_catalog_and_model(
        self,
        mocked_catalog_backend,
        item_model
    ):
        with mocked_catalog_backend as mocked_catalog:
            with mock.patch(
                'genie.wishlist.models.wishlist.WishlistModel.get'
            ) as mocked_model:
                wishlist = Wishlist('a')
                with mock.patch.object(wishlist, 'save'):
                    mocked_model.return_value = WishlistModel(
                        id='a',
                        items=[item_model]
                    )
                    await wishlist.get()

        mocked_catalog.assert_called_with(sku=item_model.sku)
        mocked_model.assert_called_with(id='a')

    async def test_get_calls_cache_and_model(self, item_model):
        with mock.patch.object(Cache, 'get') as mocked_cache:
            wishlist_model = WishlistModel(id='a', items=[item_model])
            mocked_cache.return_value = wishlist_model.to_dict()

            wishlist = await Wishlist('a').get()

        mocked_cache.assert_called_with('a')
        wishlist == wishlist_model
