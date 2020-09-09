from git import Repo

#PATH_OF_GIT_REPO = r'C:\Users\lundj\AppData\Roaming\JetBrains\PyCharmCE2020.1\scratches\.git'  # make sure .git folder is properly configured
PATH_OF_GIT_REPO = r'.'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'comment from python script'

def git_push():
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()

git_push()
