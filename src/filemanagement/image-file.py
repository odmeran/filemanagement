class ImageFile(File):
    pass
    """Image file manager.
    TO BE DELETED OR MOVED AS A SEP. PACKAGE."""
    image: np.ndarray

    def __init__(self, filename: str):
        File.__init__(self, filename)
        self.image = imread(self.get_abspath())

    def crop(self, args: str) -> None:
        """Crop image."""

        self.image = crop_image(self.image, args)

    def expand(self, args) -> None:
        """Expand image."""

        self.image = expand_image(self.image, args)

    def save(self, output_filename=None) -> str | Exception:
        """Saves file with filename specified."""

        # Set filename
        if output_filename is None:
            output_filename = self.get_name()

        # If file already exists update filename
        self.abspath = os.path.join(self.get_parent_file_name(),
                                    self.update_filename_with_version_num(output_filename))
        logger.debug("Saved as %s", self.abspath)

        try:
            imsave(self.abspath, self.image)
        except Exception as e:
            logger.error(e)
            return e

        return self.get_name()
