# Loads Data Discovered from MNET Suite and writes an Ansible Host File

#Example
#[discovered]
#10.10.10.10
#10.10.10.11
#10.10.10.11
#

# Example Mnet output - 
# "hostname","10.10.10.10","Model","12.1(22)EA10a","Serial","","IOS"
import sys, getopt
import csv

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'Arguments: -i <MNET CSV File> -o <Ansible Output File>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'Arguments -i <MNET CSV File> -o <Ansible Output File>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Processing MNET Data from:', inputfile
   print 'Ansible Host File:', outputfile
   mnet_file = open(inputfile)
   rd = csv.reader(mnet_file)

   hosts = []
   with open(outputfile,'w+') as ansible_file:
     writer = csv.writer(ansible_file)
     writer.writerow(['[discovered]'])
     for host in rd:
         writer.writerow([str(host[1])])

if __name__ == "__main__":
   main(sys.argv[1:])

