import xml.dom.minidom as dom
import time
import os


print("welcome to ODIS Dataset Maker")

dataset_lc = ['0x000240', '0x000280','0x002D00','0x000440','0x003000','0x003600','0x000DA0','0x003F00','0x002F00','0x003B00','0x007000']
dataset_information = []
number_of_ds_added = 0
dataset_lc_loopfactor = 0

def f_comma(my_str, group=2, char=',0x'):
    my_str = str(my_str)
    return char.join(my_str[i:i + group] for i in range(0, len(my_str), group))

def dataset_info():
    for i in range(len(dataset_lc)):
        dataset_user = input(f"enter dataset information for {dataset_lc[i]}\n")
        # dataset_lc_loopfactor += 1
        if dataset_user.strip() == "":
            dataset_information.append(" ")
        else:
            dataset_information.append("0x" + f_comma(dataset_user.upper()))



def missing_datasets():
    print("------------- ADDITITON OF MISSING DATASETS ------------- \nTo exit press enter \n ")
    while True:
        missing_dataset_lc = input("Please enter a dataset location: \n ")
        if missing_dataset_lc.upper() in dataset_lc:
            print(f"{missing_dataset_lc} is already known! Please use a unique name.")
            continue
        if missing_dataset_lc.rstrip() == "":
            print("Missing Dataset information complete")
            break
        else:
            print(f"Added dataset {missing_dataset_lc} to file!")
            # number_of_ds_added += 1
            dataset_lc.append(missing_dataset_lc.upper())
            new_ds = input("Please enter dataset: \n")
            dataset_information.append("0x" + f_comma(new_ds.upper()))
            print("Dataset added!")



def printing_dataset():
    print("Generating dataset")

    # Create the document object
    doc = dom.Document()

    # Create the root element
    root = doc.createElement("MESSAGE")
    doc.appendChild(root)

    # Set an attribute for the root element
    root.setAttribute("DTD", "XMLMSG")
    root.setAttribute("VERSION", "1.1")

    # Create the result element
    result = doc.createElement("RESULT")
    root.appendChild(result)

    # Create the response element
    response = doc.createElement("RESPONSE")
    result.appendChild(response)
    # set attributes to response element
    response.setAttribute("NAME", "GetParametrizeData")
    response.setAttribute("DTD", "RepairHints")
    response.setAttribute("VERSION", "1.4.7.1")
    response.setAttribute("ID", "0")

    # Create the data element
    data = doc.createElement("DATA")
    response.appendChild(data)

    # Create the request ID element
    request_ID = doc.createElement("REQUEST_ID")
    data.appendChild(request_ID)
    # Set the text for the subelement
    req_id_text = doc.createTextNode("417087939")
    request_ID.appendChild(req_id_text)

    # Create the PARAMETER_DATA element
    for i in range(len(dataset_lc)):
        if dataset_information[i].strip() == "":
            continue
        parameter_data = doc.createElement("PARAMETER_DATA")
        data.appendChild(parameter_data)
        # set attributes to response element
        parameter_data.setAttribute("DIAGNOSTIC_ADDRESS", "0x005F")
        parameter_data.setAttribute("START_ADDRESS", dataset_lc[i])
        parameter_data.setAttribute("PR_IDX", "")
        parameter_data.setAttribute("ZDC_NAME", "V03935254LN")
        parameter_data.setAttribute("ZDC_VERSION", "0001")
        parameter_data.setAttribute("LOGIN", "20103")
        parameter_data.setAttribute("LOGIN_IND", "")
        parameter_data.setAttribute("DSD_TYPE", "1")
        parameter_data.setAttribute("SESSIONNAME", "")
        parameter_data.setAttribute("FILENAME", "")
        # Set the text for the PARAMETER_DATA
        para_data_text = doc.createTextNode(str(dataset_information[i]))
        parameter_data.appendChild(para_data_text)

    # Create the compounds element
    for i in range(1, 6):
        compounds = doc.createElement("COMPOUNDS")
        data.appendChild(compounds)
        compound = doc.createElement("COMPOUND")
        compounds.appendChild(compound)
        compound.setAttribute("COMPOUND_ID", str(i))
        sw_name = doc.createElement("SW_NAME")
        compound.appendChild(sw_name)
        sw_version = doc.createElement("SW_VERSION")
        compound.appendChild(sw_version)
        sw_part_no = doc.createElement("SW_PART_NO")
        compound.appendChild(sw_part_no)

    # Create the information element
    information = doc.createElement("INFORMATION")
    data.appendChild(information)
    code_ = doc.createElement("CODE")
    information.appendChild(code_)

    # Create the DSD_DATA element
    dsd_data = doc.createElement("DSD_DATA")
    data.appendChild(dsd_data)
    compressed_data = doc.createElement("COMPRESSED_DATA")
    dsd_data.appendChild(compressed_data)
    dsd_data.setAttribute("CONTENT", "DSD-Files")
    dsd_data.setAttribute("CONTENT_TYPE", "application/tar")
    dsd_data.setAttribute("CONTENT_TRANSFER_ENCODING", "base64")
    dsd_data.setAttribute("BYTES_UNCOMPRESSED", "0")
    dsd_data.setAttribute("BYTES_COMPRESSED", "0")

    # Write the XML to a file
    # the only thing wrong with the following text is if they already called it 5f dataset, it will be overwritten still.
    # need to add a number or something after to stop it.
    xmlextension = "xml"
    while True:
        datasetgen = input("Enter a filename for the dataset? \n")
        if datasetgen.strip() == "":
            print(f"No name entered, defaulting name to: {datasetgen}")
            datasetgen = "5F Dataset"
        if os.path.exists(datasetgen):
            print(f"File {datasetgen} already exists. Not overwriting, please type another name")
        else:
            #with open(datasetgen + "." + xmlextension, "a") as f:
            with open(datasetgen + "." + xmlextension, "w", encoding="UTF-8") as f:
                f.write(doc.toprettyxml(indent="  ", encoding="UTF-8").decode())
                #f.write(doc.toprettyxml(indent="  "))
                print("Dataset created goodbye.")
                time.sleep(3)
                exit()
                break



dataset_info()
missing_datasets()
printing_dataset()