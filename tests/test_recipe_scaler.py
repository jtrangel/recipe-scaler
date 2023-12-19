import unittest
import pandas as pd
from main import scrape_recipe, scrape_recipe2
from pandas.testing import assert_frame_equal

class TestRecipeScaler(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.cookingnook.com/recipe/carbonara/'
        self.resource_path = './resources/'

    def test_1_portion(self):
        df_test1 = scrape_recipe(url=self.url, target_class='wprm-recipe-ingredient', p=1)
        df_expect1 = pd.read_csv(self.resource_path + 'test_1_portion1.csv')

        df_test2 = scrape_recipe2(url=self.url, target_class='wprm-recipe-ingredient', p=1)
        df_expect2 = pd.read_csv(self.resource_path + 'test_1_portion2.csv')

        assert_frame_equal(df_test1, df_expect1)
        assert_frame_equal(df_test2, df_expect2)

    def test_50_portions(self):
        df_test1 = scrape_recipe(url=self.url, target_class='wprm-recipe-ingredient', p=50)
        df_expect1 = pd.read_csv(self.resource_path + 'test_50_portion1.csv')

        df_test2 = scrape_recipe2(url=self.url, target_class='wprm-recipe-ingredient', p=50)
        df_expect2 = pd.read_csv(self.resource_path + 'test_50_portion2.csv')

        assert_frame_equal(df_test1, df_expect1)
        assert_frame_equal(df_test2, df_expect2)

    def test_100_portions(self):
        df_test1 = scrape_recipe(url=self.url, target_class='wprm-recipe-ingredient', p=100)
        df_expect1 = pd.read_csv(self.resource_path + 'test_100_portion1.csv')

        df_test2 = scrape_recipe2(url=self.url, target_class='wprm-recipe-ingredient', p=100)
        df_expect2 = pd.read_csv(self.resource_path + 'test_100_portion2.csv')

        assert_frame_equal(df_test1, df_expect1)
        assert_frame_equal(df_test2, df_expect2)
