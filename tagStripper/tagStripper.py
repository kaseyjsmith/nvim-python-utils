#!/Users/kasey.smith/.venvs/obsidian/bin/python3

import yaml, os, re, sys

class TagStripper:
    def __init__(self):
        self.dirs = self.getDirs()
        self.tags = self.getTags()
        self.files = self.getFiles()

    def getDirs(self):
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        # Append $HOME to the directories
        config['dirs'] = [f'{os.environ["HOME"]}{dir}' for dir in
                          config['dirs']]
        return config['dirs']

    def getTags(self):
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config['tags']

    def checkTags(self, line):
        for tag in self.tags:
            if tag in line:
                return True
        return False

    def checkDone(self, line):
        if '[x]' in line:
            return True
        return False

    def checkDeferred(self, line):
        if '[>]' in line:
            return True
        return False

    def getFiles(self):         # TODO: clean this up
        files = []
        for dir in self.dirs:
            # Loop through files in the directory
            # print(f"Checking {dir} for markdown files")
            # print(os.listdir(dir))
            for file in os.listdir(dir):
                # Check for markdown files
                if file.endswith('.md'):
                    # Open the file
                    # print(f"Checking {file} for tags")
                    with open(f'{dir}/{file}', 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            # Check for tags
                            if self.checkTags(line):
                                files.append(f'{dir}{file}')
                                # Break out of the loop if a tag is found
                                break
        return files

    def stripTags(self):
        # TODO: add handling for:
        # follow up, canceled, etc.
        for file in self.files:
            with open(file, 'r+') as f:
                lines = f.readlines()

                for idx, line in enumerate(lines):
                    for tag in self.tags:
                        if self.checkDone(line) and self.checkTags(line):
                            # print(f"Tag found in {file}")
                            # print(line)
                            lines[idx] = re.sub(rf'{tag}', '', line)
                            # print(f'Line after stripping: \n{line}')
                        if self.checkDeferred(line) and not line.__contains__("#deferred"):
                            lines[idx] = line.replace('\n', ' #deferred\n')


                f.seek(0)
                f.truncate()
                for line in lines:
                    f.write(line)
                f.close()

if __name__ == '__main__':
    ts = TagStripper()

    # create a backup of the current files in the vault
    os.system(
            f"""
            tar -czf \
            ~/Documents/notes/backups/tagStripper_backup_$(date +%Y-%d-%m_%T).tar.gz \
            {" ".join([str(x) for x in ts.files])}"""
            )

    ts.stripTags()
