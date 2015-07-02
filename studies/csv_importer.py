#encoding: utf-8
import csv
from models import Candidate, Study, Assignment
from requisitions.models import Requisition

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

def import_data(datafile):
	base_dir = settings.BASE_DIR+settings.MEDIA_URL+'uploads/massive/'
	path = default_storage.save(base_dir+'temp.csv', ContentFile(datafile.read())) 
	
	dataReader = csv.reader(open(path, 'rU'), delimiter=';', quotechar='"')


	for row in dataReader:
		
		if row[0] != 'NumeroRequisicion':
			requisition = Requisition.objects.get(id=row[0])
			print requisition.id

			candidate = Candidate(
				dni=row[1],
				first_name=unicode(row[2]),
				last_name='Gómez'.decode('utf-8'),
				phone=row[4],
				mobile=row[5],
				email=row[6],
				address=row[7],
				aspired_role=row[8]
			)
			candidate.candidate_photo = 'uploads/avatars/candidates/candidate.png'
			candidate.save()

			study = Study(requisition=requisition, candidate=candidate)
			study.save()

			employee = User.objects.get(id=row[9])
			assignment = Assignment(study=study, employee=employee)
			assignment.save()

	os.remove(path) 

