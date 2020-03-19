from simple_settings import settings

from genie.backends.pools.database import DatabaseBackendPool


def mirgate():
    import ipdb
    ipdb.set_trace()
    database = DatabaseBackendPool.get(
        backend_id=settings.DEFAULT_DATABASE_BACKEND
    )

    """
        -- Schema genie
    """
    database._execute("""
        CREATE SCHEMA IF NOT EXISTS `genie` DEFAULT CHARACTER SET utf8 ;
        USE `genie` ;
    """)

    """
    -- Table `genie`.`Wishlist`
    """
    database._execute("""
        CREATE TABLE IF NOT EXISTS `genie`.`Wishlist` (
          `id` INT NOT NULL,
          `wishlist_id` VARCHAR(45) NULL,
          PRIMARY KEY (`id`))
        ENGINE = InnoDB;
    """)

    """
    -- Table `genie`.`WishlistItem`
    """
    database._execute("""
        CREATE TABLE IF NOT EXISTS `genie.`.`WishlistItem` (
          `id` INT NOT NULL,
          `sku` VARCHAR(45) NULL,
          `title` VARCHAR(45) NULL,
          `image_url` VARCHAR(45) NULL,
          `price` VARCHAR(45) NULL,
          `brand` VARCHAR(45) NULL,
          `review_score` VARCHAR(45) NULL,
          `wishlist` INT NULL,
          PRIMARY KEY (`id`),
          INDEX `wishlist_idx` (`wishlist` ASC) VISIBLE,
          CONSTRAINT `wishlist`
            FOREIGN KEY (`wishlist`)
            REFERENCES `genie`.`Wishlist` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;
    """)

    """
    -- Table `genie`.`Customer`
    """
    database._execute("""
        CREATE TABLE IF NOT EXISTS `genie`.`Customer` (
          `id` INT NOT NULL,
          `customer_id` VARCHAR(45) NULL,
          `name` VARCHAR(100) NULL,
          `email` VARCHAR(45) NULL,
          `wishlist` INT NULL,
          PRIMARY KEY (`id`),
          INDEX `wishlist_idx` (`wishlist` ASC) VISIBLE,
          CONSTRAINT `wishlist`
            FOREIGN KEY (`wishlist`)
            REFERENCES `genie`.`Wishlist` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB;
    """)

    database._execute("""
        SET SQL_MODE=@OLD_SQL_MODE;
        SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
        SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
    """)
