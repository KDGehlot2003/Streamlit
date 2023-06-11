import streamlit as st
from pathlib import Path
from pdf2image import convert_from_path
import easyocr
import re
from datetime import datetime
import os
from PIL import Image
import time 

st.title("Extract details from pdf")
# st.image(res, width = 800)

st.markdown("**Please upload the pdf :**")
with st.form(key="Form :", clear_on_submit = True):
    # Name = st.text_input("Name : ")
    # Email = st.text_input("Email ID : ")
    File = st.file_uploader(label = "Upload file", type=["pdf","docx"])
    Submit = st.form_submit_button(label='Submit')
    

    


# st.subheader("Details : ")
# st.metric(label = "Name :", value = Name)
# st.metric(label = "Email ID :", value = Email)

if Submit :

    st.markdown("**The file is sucessfully Uploaded.**")

    # Save uploaded file to 'F:/tmp' folder.
    save_folder = '/home/kdgehlot/Desktop/temp'
    save_path = Path(save_folder, File.name)
    with open(save_path, mode='wb') as w:
        w.write(File.getvalue())

    if save_path.exists():
        st.success(f'File {File.name} is successfully saved!')

    
    global scanned_text
    global result
    
    
    images = convert_from_path(f'/home/kdgehlot/Desktop/temp/{File.name}',dpi=300)
    
    
    for i in range(len(images)):
    
        images[i].save('page'+ str(i) +'.jpg', 'JPEG')
    
    len_of_image = len(images)
    
    def compress(image_file):
    
        filepath = os.path.join(os.getcwd(), image_file)
    
        image = Image.open(filepath)
    
        image.save("image-file-compressed",
                     "JPEG",
                     optimize = True,
                     quality = 10)
        return
    
    
    
        
    compress('page0.jpg')
    
    
    reader = easyocr.Reader(['en'], gpu=False) 
    result = reader.readtext('image-file-compressed', detail=0)
    
    with open('converted.txt',mode ='w') as file:
        file.write("converted.txt \n \n")
    
    
    for i in result:
        with open('converted.txt',mode ='a') as file:
            file.write(i)
            file.write("\n")
            scanned_text = i
            # print(scanned_text)
    
    
    
    def extract_date_from_pdf():
        
        extracted_dates = []
    
        for i in result:
            date_pattern = r'\b\d{1,2}-[A-Za-z]{3}-\d{2}\b'   # Example date pattern: 1-may-22
            dates = re.findall(date_pattern, i)
            extracted_dates.extend(dates)
            # print(dates)
            # print(date_pattern)
    
        return extracted_dates
    
    def extract_invoice_no_from_pdf():
        
        extracted_invoice_no = []
    
        for i in result:
            invoice_no_pattern = r'[A-Za-z]{2}\/\d{2}-\d{2}\/\d{3}|[A-Za-z]{2}\/\d{4}-\d{2}\/\d{4}|\d{4}-\d{2}\/\d{4}|\d{4}-\d{2}\/\d{3}'
            invoices = re.findall(invoice_no_pattern, i)
            extracted_invoice_no.extend(invoices)
    
        return extracted_invoice_no
    
    
    def extract_PO_no_from_pdf():
        
        extracted_PO_no = []
    
        for i in result:
            PO_no_pattern = r'^\d{10}$'
            POs = re.findall(PO_no_pattern, i)
            extracted_PO_no.extend(POs)
    
        return extracted_PO_no
    
    
    
    def extract_rate_from_pdf():
        
        extracted_rate = []
    
        for i in result:
            PO_no_pattern = r'\d{1,3}(?:,\d{3})*\.\d{2}'
            POs = re.findall(PO_no_pattern, i)
            extracted_rate.extend(POs)
    
        return extracted_rate
    
    
    rts = extract_rate_from_pdf()
    rts = [value.replace(',', '') for value in rts]
    rts = [float(value) for value in rts]
    list2 = list(set(rts))
    list2.sort()
    print(list2)
    high_rt = list2[-1]
    sec_high_rt = list2[-2]
    t_rate_gst = "{:,.2f}".format(high_rt)
    
    t_rate = "{:,.2f}".format(sec_high_rt)
    st.markdown(f"**Total Rate:** {t_rate_gst}")
    st.markdown(f"**Total Rate without gst:** {t_rate}")
    
    
    dates = extract_date_from_pdf()
    dt_lst = []
    for i in dates:
        date_object = datetime.strptime(i, '%d-%b-%y').date()
        dt = date_object.strftime("%d.%m.%Y")
        dt_lst.append(dt)
    max_dt = max(dt_lst)
    try:
        if max_dt!=None:
            st.markdown(f"**date:** {max_dt}")
        else:
            st.markdown("Date No. : CAN'T FIND THE VALUE ")
    except:
        st.markdown("date error")
    
    
    # for date in dates:
    #     date_object = datetime.strptime(date, '%d-%b-%y').date()
    #     dt = date_object.strftime("%d.%m.%y")
    #     print("date: ",dt)
    
    invoices = extract_invoice_no_from_pdf()
    # for invoice in invoices:
    try:
        if invoices!=None:
            st.markdown(f"**Invoice No. :** {invoices[0]}")
        else:
            st.markdown("Invoice No. : CAN'T FIND THE VALUE ")
    except:
        st.markdown("Invoice error")
    
    POs = extract_PO_no_from_pdf()
    # for PO in POs:
    try:
        if POs!=None:
            st.markdown(f"**PO No. :** {POs[0]}")
        else:
            st.markdown("PO No. : CAN'T FIND THE VALUE ")
    except:
        st.markdown("PO error")
    
    
    