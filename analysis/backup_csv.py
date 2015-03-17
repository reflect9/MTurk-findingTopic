from subprocess import call

path_csv = "csv_backup_3"
tables_to_backup = ["Answer","TaskCounter","LabelingHit"]



loader = "bulkloader.py"
template = " --download --url http://findingtopic.appspot.com/_ah/remote_api --config_file generated_bulkloader.yaml --kind %s --filename %s/%s.csv"

for table in tables_to_backup:
	options = (template % (table,path_csv,table))
	print options
	# call("bulkloader.py")
	call(loader + " "+ options, shell=True)
