import os, sys, argparse, re
from git import Repo

class Logger:
    def __init__(self, save_dir=None, save_dir_key='--save_dir', parsed_args=None):
        # 引数をパースしたやつが入る
        self.arg_dict = dict()
        self.exec_command = sys.argv[0]
        self.parse_args(parsed_args)

        # save_dir_key　save_dir を引数に応じて変更する
        self.save_dir_key = self.remove_head_hyphen(save_dir_key)

        self.save_dir =save_dir
        # save_dir が優先される。
        if save_dir != None:
            self.save_dir = self.arg_dict[self.save_dir_key]

        # ディレクトリ作ってくれるやつ。
        self.create_dir()
        self.git = GitHandler()

        self.untracked_file_contents = self.untracked_file_contents()
        self.export_result_file()

    def create_dir(self):
        if not os.path.exists(self.save_dir[0]):
            os.mkdir(self.save_dir[0])

    def remove_head_hyphen(self, save_dir_key):
        # オプションの先頭のハイフンをなくす。
        if save_dir_key[0] == '-':
            save_dir_key = save_dir_key[1:]
            return self.remove_head_hyphen(self.remove_head_hyphen(save_dir_key))
        return save_dir_key

    def parse_args(self, args):
        arg_dict = dict()
        for arg in vars(args):
            arg_dict[arg] = []
            arg_dict[arg].append(getattr(args, arg))
        self.arg_dict = arg_dict


    def untracked_file_contents(self):
        self.untracked = []
        untracked_files = self.git.untracked
        for i in untracked_files:
            if i == os.path.join(self.save_dir[0], 'result_for_exp_with_git_info.txt')[2:]:
                continue
            with open(i, 'r') as r:
                self.untracked.append(r.read())


    def export_result_file(self):
        from datetime import datetime
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        with open(os.path.join(self.save_dir[0], 'result_for_exp_with_git_info.txt'), 'w') as f:
            f.write('executed on {0} \n'.format(now))
            f.write('\n')
            f.write('###############################################\n')
            f.write('latest_log name: {0}\n'.format(self.git.latest_log))
            f.write('\n')
            f.write('###############################################\n')
            f.write('branch name: {0}\n'.format(self.git.branch.name))
            f.write('\n')
            f.write('###############################################\n')
            f.write('untracked: {0}\n'.format(self.git.untracked))
            f.write('\n')
            f.write('###############################################\n')
            f.write('diffs: {0}\n'.format(self.git.diff_commit))
            f.write('\n')
            f.write('###############################################\n')
            f.write('\n')
            f.write('contents of untracked files:\n')
            f.write('\n')
            for i in range(len(self.untracked)):
                f.write('untracked {0}: \n{1}\n'.format(i, self.untracked[i]))

class GitHandler:
    def __init__(self):
        self.repo = self.initialize_repo()
        self.branch = self.get_branch()
        self.log = self.get_log()
        self.latest_log = self.get_latest_log()
        self.diff_commit = self.get_diff_in_currend_branch()
        self.untracked = self.repo.untracked_files


    def initialize_repo(self):
        return Repo('./')

    def get_branch(self):
        return self.repo.active_branch

    # def git_status(self):
    #     pass
    #
    def get_log(self):
        return self.repo.head.reference.log()

    def get_latest_log(self):
        return self.log[-1].newhexsha

    def get_diff_in_currend_branch(self):
        return self.repo.git.diff(self.repo.head.commit.tree)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--save_dir', default='./result')
    parser.add_argument('--train_or_test', default='train')
    args = parser.parse_args()
    logger = Logger(parsed_args=args, save_dir='--save_dir')
