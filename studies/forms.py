from django import forms
from models import Candidate, Study

class CandidateForm(forms.ModelForm):
	class Meta:
		model = Candidate
		
		fields = '__all__'

class StudyForm(forms.ModelForm):

	class Meta:
		model = Study
		fields = '__all__'
