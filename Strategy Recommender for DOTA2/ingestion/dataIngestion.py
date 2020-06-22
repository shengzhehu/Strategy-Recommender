import subprocess
import sys

class DataIngestion(object):
    def __init__(self,fname):

        """
        """

        self.bucket = "dotamatches"
        self.filename = fname
        ## split the date string into year, month, day string format


    def import_data_to_S3(self):

        """
        Download the data file from the torrent file;
        Save it temporarily on machine and extract .csv file;
        Return the gzipped file name;
        """

        gzfile = self.filename
        subprocess.run(["aws", "s3", "cp", gzfile, "s3://{Bucket}/".format(Bucket = self.bucket)])
        subprocess.run(["rm", gzfile])

    def run(self):
        self.import_data_to_S3()
        print("Finish importing data to S3!")

def main():
    date = sys.argv[1]
    proc = DataIngestion(fname)
    proc.run()

main()
