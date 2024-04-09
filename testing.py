import unittest
from regex_method.regex_method_driver import RegexMethodPipeline
from api_method.api_method_driver import ApiMethodPipeline
from polling_data.polling_data_compiler import PollingDataCompiler

class TestRegexMethodPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = RegexMethodPipeline(
            API_KEY="9jleO955LNYEMxbaH5A49adGcBJle43K",
            START_YEAR=2000,
            END_YEAR=2022
            )

    def test_run_main(self):
        self.pipeline.run_main()
        self.pipeline.graph_data()
    
    def test_load_main(self):
        self.pipeline.load_main()
        self.pipeline.graph_data()

    def test_run_stats(self):
        self.pipeline.run_stats()
        
    def test_load_stats(self):
        self.pipeline.load_stats()

class TestApiMethodPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ApiMethodPipeline(
            API_KEY="9jleO955LNYEMxbaH5A49adGcBJle43K",
            START_YEAR=2000,
            END_YEAR=2022
            )
        
    def test_pull_data(self):
        self.pipeline.run()
        self.pipeline.graph_data()

    def test_load_data(self):
        self.pipeline.load_data()

class TestPollingDataCompiler(unittest.TestCase):
    def setUp(self):
        self.pipeline = PollingDataCompiler(
            FILE = "assets/roper-folder-toplines-asof-20230127.csv"
        )
    
    def test_run(self):
        self.pipeline.run()

if __name__ == '__main__':
    unittest.main()
