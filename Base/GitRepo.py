from git import Repo


class Repository:
    # rorepo is a Repo instance pointing to the git-python repository.
    # For all you know, the first argument to Repo is a path to the repository
    # you want to work with
    def __init__(self,path:str):
        self.my_repo = Repo(self.rorepo.working_tree_dir);
        assert not self.my_repo.bare

    def Creat(self, name:str)->bool:
        result: bool = True;
        return (result);

    def Clone(self)->bool:
        result:bool = True;
        return(result);