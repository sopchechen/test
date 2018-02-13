from Queue import PriorityQueue
from math import ceil
import sys
class donation_analysis():
	def __init__(self,itcont_file,percentile_file,output_file):
		# transaction record is the hash table of the content in itcont.txt
		# key : CMTE_ID + ZIP_CODE + year
		# value : lists of [donor's name, transaction amount, the month and date]
		self.transaction_record = {}
		# donor_list is the hash table of all information about donors     
		# key : donor's name(NAME) + ZIP_CODE
		# value : lists of [CMTE_ID,TRANSACTION_MT, year,month_date]   
		self.donor_list = {}
		# donor_min_year is a hash table used to indicate the first year that the donor make a donation
		# key: NAME + ZIP_CODE
		# value: year
		self.donor_min_year = {}
		# the following are all index of certain value in the line of itcont.txt
		self.CMTE_ID_ind = 0           # CMTE_ID
		self.NAME_ind = 7              # donor's name
		self.ZIP_CODE_ind = 10         # ZIP_CODE
		self.TRANSACTION_DT_ind = 13   # transaction date
		self.TRANSACTION_MT_ind = 14   # transaction amount
		self.OTHER_ID_ind = 15         # other ID


		self.percentile = self.load_percentile(percentile_file)
		self.process_transaction_data(itcont_file,output_file)


	# load the percentile from percentile.txt and store it in self.percentile
	def load_percentile(self,percentile_file):
		with open(percentile_file) as f:
			for line in f:
				percentile = float(line)/100.0
		f.close()
		return percentile

	# find the ordinal rank through the nearest-rank method
	def find_percentile_ind(self,num_of_contribution):
		return int(ceil(self.percentile*num_of_contribution))

	''' 
	The steps in function process_transaction_data():
	 1. read itcont.txt line by line
	    We treat each line in itcont.txt as a record
	 2. If the record is valid, store it in self.transaction_record and self.donor_list
     3. If the record comes from a repeat donor, 
        check the self.transaction_record and output the requested calculations
     4. repeat the above steps until reach the end of itcont.txt 
	'''
	def process_transaction_data(self,itcont_file,output_file):
		with open(output_file,'w') as output_f:
			with open(itcont_file) as input_f:
				for line in input_f:
					line = line.split('|')
					# check whether the record is valid
					if self.isValid(line):
						# store values form fields that we are interested in
						CMTE_ID = line[self.CMTE_ID_ind]
						ZIP_CODE = line[self.ZIP_CODE_ind][0:5]
						NAME = line[self.NAME_ind]
						TRANSACTION_DT = line[self.TRANSACTION_DT_ind]
						TRANSACTION_MT = int(line[self.TRANSACTION_MT_ind])

						year = int(TRANSACTION_DT[4:8])
						month_date = int(TRANSACTION_DT[0:4])

						# store those values in self.transaction_record
						transaction_key = CMTE_ID + ZIP_CODE + str(year)
						if transaction_key not in self.transaction_record:
							self.transaction_record[transaction_key] = [[NAME,TRANSACTION_MT, month_date]]
						else:
							self.transaction_record[transaction_key].append([NAME,TRANSACTION_MT, month_date])
						
						# store those value in self.donor_list and self.donor_min_year
						donor_key = NAME + ZIP_CODE
						if donor_key not in self.donor_list:
							self.donor_list[donor_key] = [[CMTE_ID,TRANSACTION_MT,year,month_date]]
							self.donor_min_year[donor_key] = year
						else: # the donor is a repeat donor
							self.donor_list[donor_key].append([CMTE_ID,TRANSACTION_MT,year,month_date])

							'''
							If this is a second donation and it have a transaction date that is from 
							a previous calendar year, print the later donation. 
							'''
							if len(self.donor_list[donor_key]) == 2 and self.donor_list[donor_key][0][2] > year:
								line = self.printrecord(self.donor_list[donor_key][0][0],ZIP_CODE,self.donor_list[donor_key][0][2])
								output_f.write(line)
								self.donor_min_year[donor_key] = year
							else:
								'''
								If the donation's transaction year is not the earliest, output the requested calculations 
								for that calendar year, zip code and receipient. 
								'''
								if year >= self.donor_min_year[donor_key]:
									output_line = self.printrecord(CMTE_ID,ZIP_CODE,year)
									output_f.write(output_line)
								else:
									self.donor_min_year[donor_key] = year
			input_f.close()
		output_f.close()

	# output the requested calculations for that calendar year, zip code and recipient 
	def printrecord(self,CMTE_ID,ZIP_CODE,year):
		key = CMTE_ID + ZIP_CODE + str(year)
		record  = self.transaction_record[key]
		q = PriorityQueue() # used proirity queue to sort the transaction according to the transaction date
		num_of_contribution = 0
		amt_of_contribution = 0
		for single_record in record:
			[NAME,TRANSACTION_MT,month_date] = single_record
			if len(self.donor_list[NAME+ZIP_CODE]) > 1:
				q.put((month_date,TRANSACTION_MT))
				num_of_contribution+=1
				amt_of_contribution+=TRANSACTION_MT
		percentile_ind = self.find_percentile_ind(num_of_contribution)
		run_percentile = q.queue[percentile_ind-1]
		line = CMTE_ID + '|' + ZIP_CODE +'|' + str(year) + '|'+ str(int(round(run_percentile[1]))) +'|' + str(amt_of_contribution) + '|' + str(num_of_contribution) + '\n'
		# print line
		return line


	# check whether the line in itcont.txt is valid
	def isValid(self,line):
		checkingA = self.CMTE_ID_isvalid(line[self.CMTE_ID_ind]) and self.NAME_isvalid(line[self.NAME_ind]) and self.ZIP_CODE_isvalid(line[self.ZIP_CODE_ind])
		checkingB = self.TRANSACTION_DT_isvalid(line[self.TRANSACTION_DT_ind]) and self.TRANSACTION_MT_isvalid(line[self.TRANSACTION_MT_ind]) and self.other_ID_isvalid(line[self.OTHER_ID_ind]) 
		return checkingA and checkingB

    # check whether CMTD_ID is empty
	def CMTE_ID_isvalid(self,CMTE_ID):
		return (CMTE_ID != '')  

	# check whether the donor's name is empty or malformed
	def NAME_isvalid(self,NAME):
		if NAME == '':     
			return False
		for i in NAME:
			if i.isdigit():
				return False
		return True

	# check whether the zip code is less than 5 digits
	def ZIP_CODE_isvalid(self,ZIP_CODE):
		return (len(ZIP_CODE) >= 5) 

	# check whether the transaction data is a valid date
	def TRANSACTION_DT_isvalid(self,TRANSACTION_DT):
		if len(TRANSACTION_DT) != 8:
			return False
		date = int(TRANSACTION_DT[0:2])
		month = int(TRANSACTION_DT[2:4])
		year = int(TRANSACTION_DT[4:8])
		return (date <= 12 and month <= 31 and year <= 2018) 

	# check whether the transaction amount is empty
	def TRANSACTION_MT_isvalid(self,TRANSACTION_MT):
		return (TRANSACTION_MT != '')

	# check whether OTHER_ID is empty
	def other_ID_isvalid(self,OTHER_ID):
		return (OTHER_ID == '')

itcont_file = sys.argv[1]
percentile_file = sys.argv[2]
output_file = sys.argv[3]
res = donation_analysis(itcont_file,percentile_file,output_file)


