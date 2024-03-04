import csv
from datetime import datetime
import requests

def map_gender(gender):
    mapping = {
        "Masculino": "male",
        "Feminino": "female",
        "Outro": "other",
    }

    return mapping.get(gender, "unknown")

def date_format(date):
    return datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')

def create_patient(name, cpf, gender, birth_date, phone, birth_country):
    patient = {
                "resourceType": "Patient",
        "id": "example",
        "identifier": [
            {
                "use": "usual",
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "BR"
                        }
                    ]
                },
                "system": "urn:oid:1.2.36.146.595.217.0.1",
                "value": cpf,
                "period": {
                    "start": date_format(birth_date)
                },
                "assigner": {
                    "display": "Sistema de Identificação do Brasil"
                }
            }
        ],
        "active": True,
        "name": [
            {
                "use": "official",
                "family": name.split()[1],
                "given": [name.split()[0]]
            }
        ],
        "telecom": [
            {
                "system": "phone",
                "value": phone,
                "use": "mobile",
                "rank": 1
            }
        ],
        "gender": map_gender(gender),
        "birthDate": date_format(birth_date),
        "deceasedBoolean": False,
        "address": [
            {
                "use": "home",
                "type": "both",
                "country": birth_country
            }
        ],
        "extension": [
            {
                "url": "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRNacionalidade",
                "valueCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://www.saude.gov.br/fhir/r4/ValueSet/BRNacionalidade-1.0",
                            "code": "BR",
                            "display": "Brasileiro"
                        }
                    ]
                }
            },
             {
                "url": "http://hl7.org/fhir/StructureDefinition/patient-birthPlace",
                "valueString": birth_country
            }
        ]
    }
    return patient

def create_observation(patient_id, observation_text):
    observation = {
        "resourceType": "Observation",   
        "status": "final",   
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "60591-5",
                    "display": "Patient summary"
                }
            ],
            "text": "Patient summary"
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "valueString": observation_text 
    }
    return observation

def reset_database():
    get_all_endpoint = 'http://localhost:8080/fhir/Patient'
    response = requests.get(get_all_endpoint)
    get_all_observation_endpoint = 'http://localhost:8080/fhir/Observation'
    response_observation = requests.get(get_all_observation_endpoint)

    if response_observation.status_code == 200:
        observations = response_observation.json().get('entry')
        for observation in observations:
            observation_id = observation.get('resource').get('id')
            delete_observation_endpoint = f'http://localhost:8080/fhir/Observation/{observation_id}'
            response_delete_observation = requests.delete(delete_observation_endpoint)

            if response_delete_observation.status_code == 200:
                print(f"Observation {observation_id} deleted successfully.")
            else:
                print(f"Failed to delete Observation {observation_id}. Response status:", response_delete_observation.status_code)
                print("Response text:", response_delete_observation.text)

    if response.status_code == 200:
        patients = response.json().get('entry')
        for patient in patients:
            patient_id = patient.get('resource').get('id')
            delete_patient_endpoint = f'http://localhost:8080/fhir/Patient/{patient_id}'
            response_delete_patient = requests.delete(delete_patient_endpoint)

            if response_delete_patient.status_code == 200:
                print(f"Patient {patient_id} deleted successfully.")
            else:
                print(f"Failed to delete Patient {patient_id}. Response status:", response_delete_patient.status_code)
                print("Response text:", response_delete_patient.text)

def main():
    csv_file = "patients.csv" 

    # Read the CSV file to get the data and create the patients/observations
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Nome']
            cpf = row['CPF']
            gender = row['Gênero']
            birthdate = row['Data de Nascimento']
            phone = row['Telefone']
            birth_country = row['País de Nascimento']

            observation = row['Observação']

            # Creating the patient data
            patient = create_patient(name, cpf, gender, birthdate, phone, birth_country) 
            print(patient)

            # Request to create the patient sending the patient data
            create_patient_endpoint = 'http://localhost:8080/fhir/Patient'
            response_create_patient = requests.post(create_patient_endpoint, json=patient) 
                
            if response_create_patient.status_code == 201:
                patient_id = response_create_patient.json().get('id') 
                print("Patient created successfully. Patient ID:", patient_id)
                
                # Check if the observation is not empty
                if observation.strip():
                    observation_data = create_observation(patient_id, observation)
                    # Request to create the observation
                    create_observation_endpoint = 'http://localhost:8080/fhir/Observation'
                    response_observation = requests.post(create_observation_endpoint, json=observation_data)
                    
                    # Check if the observation was created successfully
                    if response_observation.status_code == 201:
                        print("Observation created successfully.")
                    else:
                        print("Failed to create Observation. Response status:", response_observation.status_code)
                        print("Response text:", response_observation.text)
                else:
                    # If the observation is empty, print a message   
                    print("No Observation provided. Skipping Observation creation.")
            else:
                print("Failed to create Patient. Response status:", response_create_patient.status_code)
                print("Response text:", response_create_patient.text)
            # Print a separator
            print("=" * 80)

if __name__ == "__main__":
    main()