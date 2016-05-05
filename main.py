"""
Main class of the GithubTracker project
"""
import References.Semester as Repositories
import Utilities.Parsers as Parsers
import Utilities.Login as Login
import Statistics.Statistics as stats
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"

login = Login.Login()

manager = login.get_user()

repositories = Parsers.parse_repositories(manager, Repositories.fall16_projects)

statistics = stats.Statistics(repositories, Repositories.fall16)

statistics.calculate()

# TODO Get statistics from repositories
print "done"

