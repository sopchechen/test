# Donation Analytics #

## General Idea ##
I use python to solve the problem, and there is a source code called donation-analysis.py in the source file.
My program will read records in `incont.txt` line by line. When the program read a new record, it will do:
1. check whether all fields that we are interested in are valid
2. if all fields are valid, store the record in two hash tables called `transaction_record` and `donor_list`
3. check the number of record in `donor_list` with key value `NAME` + `ZIP_CODE`
4. if there are more than one record in `donor_list[NAME + ZIP_CODE]`, the donor is a repeat donor, go to step 5, otherwise, go to step 6
5. using `CMTE_ID` , `ZIP_CODE` and `year` as a key, call the function called `printrecord()` to output the requested calculations  
6. repeat step 1-5 until read the end of file


## Date Structure ##
I use two hash tables called `transaction_record` and `donor_list` to store records.<br/> 
* In `transaction_record`, if contributions have same recipient, zip code and calender year, they will be listed together. The key of `transaction_record` is `CMTE_ID`+`ZIP_CODE`+`year`, and the corresponding value are lists of ( or maybe only one list ) `[NAME,TRANSACTION_MT, month_date]` <br/> 
* In `donor_list`, all contributions from same donor will map to same key. The key is `NAME + ZIP_CODE`, and the value are lists (or maybe one list) of `[CMTE_ID,TRANSACTION_MT,year,month_date]`

People may wonder why we store same record two times. Although creating two hash tables which store same data may waste some space, the time complexity can reduce a lot when we find data we need and output the requested calculations.

## Function ##
All functions are in a class called `donation_analysis()`, what they have to do is:
* `load_percentile()`: It load the percentile from percentile.txt and store it in self.percentile
* `find_percentile_ind()`: It find the ordinal rank through the nearest-rank method
* `process_transaction_data():` load records from `incont.txt` and store them in two hash tables. It will called `printrecord()` when the      new record is from a repeat donor.
* `printrecord()`: Given `CMTE_ID`,`ZIP_CODE` and `year` It uses priority queue to sort the contribution from repeat donors by the transaction month and list all output data.
* `isValid()`: check whether the new record has correct format

## How to run the program ##
There is only one program called donation-analysis.py in the source file. It doesn't require additional libraries, environments, or dependencies, Users can run the program through run.sh.

