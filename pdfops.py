"""
This is a PDF filling program. It will include functions for writing using dict,
for writing and locking using dict, for locking without dict, for unlocking 
without dict. 

This satisfies requirements for the monthly reappointment letter process, 
PAF creation, and also for fixing accidents (like filling out and sighning a 
template rather than making a Save As copy).

This program assumes that it may be used for multipage PDFs and further assumes
taht each page will have uniquely named fields with no overlap. Fields sharing
the same name and automatically enumerated by Adobe cannot be filled out by
this method and duplicated field names will cause collisions in the dictionary.
"""

import pdfrw
#TODO find out about read-only versions non-read only versus locking 

def pdf_writer(input_pdf_path,output_pdf_path=None, data_dict=None,lock=None):
    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = '/Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotation_col=[]    
    for page in template_pdf.pages:
        annotation_col.append(page[ANNOT_KEY])
    if data_dict:
        data_dict=data_dict
    else: 
        data_dict={}  #creating empty dict, won't trigger later if statement
    
    for annotations in annotation_col:
        for annotation in annotations:
            key = annotation[ANNOT_FIELD_KEY][1:-1]
            if key in data_dict.keys():
                try:
                    annotation.update(
                    pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                )
                except:
                    print("didn't work boss")
            if lock:
                if lock==False:
                   annotation.update(pdfrw.PdfDict(Ff=0))
                if lock==True:
                   annotation.update(pdfrw.PdfDict(Ff=1)) 
    if output_pdf_path:
        output_pdf_path=output_pdf_path
    else:
        output_pdf_path=input_pdf_path
    
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'))) 
    pdfrw.PdfWriter().write(input_pdf_path, template_pdf)        


def write_fillable_pdf(input_pdf_path, outfile, data):
    pdf_writer(input_pdf_path, output_pdf_path=outfile, data_dict=data,lock=True)
    
def write_fillable_unlocked(input_pdf_path, outfile, data):
    pdf_writer(input_pdf_path, output_pdf_path=outfile, data_dict=data,lock=False)
    #rightfully, this function should be named write_fillable_pdf, but dependencies.
def lock_pdf(input_pdf_path):
   pdf_writer(input_pdf_path,lock=True)
   
def unlock_pdf(input_pdf_path):
   pdf_writer(input_pdf_path,lock=False)

#TODO write reader that returns structured data, fields and adjacent text?
