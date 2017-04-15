import os
import shutil

from django.test import TestCase, override_settings

from maker.models import App, Repository
from . import TEST_DIR


@override_settings(MEDIA_ROOT=TEST_DIR)
class AppTestCase(TestCase):

    def setUp(self):
        # Create Repository
        repository = Repository(name="Test", description="Test", url="https://f-droid.org",
                                user_id=1)
        repository.save()

        # Create App
        app = App.objects.create(repo=repository)

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def test_icons_get_deleted_from_repo(self):
        # Get app
        app = App.objects.get(id=1)

        # Get icon name
        icon_name = os.path.basename(app.icon.path)

        # Get path of repository
        path = app.repo.get_repo_path()

        # Go through every item in repository
        for item in os.listdir(path):

            # Only use directories that start with "icons"
            if os.path.isdir(os.path.join(path, item)) and 'icons' in item:

                # Check that icons exist
                icon = os.path.join(path, item, icon_name)
                self.assertTrue(os.path.isfile(icon))

        # Delete app icons
        app.delete_app_icons_from_repo()

        # Go through every item in repository
        for item in os.listdir(path):

            # Only use directories that start with "icons"
            if os.path.isdir(os.path.join(path, item)) and 'icons' in item:

                # Check that icons do not exist anymore
                icon = os.path.join(path, item, icon_name)
                self.assertFalse(os.path.isfile(icon))
