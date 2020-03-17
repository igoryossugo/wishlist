import os

import vcr
from simple_settings import settings

cassettes_dir = os.path.join(settings.BASE_PATH, 'tests', 'fixtures/cassettes')
vcr_client = vcr.VCR(
    serializer='json',
    cassette_library_dir=cassettes_dir,
    record_mode='once',
    match_on=['uri', 'method'],
    ignore_localhost=True,
)
