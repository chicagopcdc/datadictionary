All the ontologies terms are saved in the _terms.yaml file with the format {ontology_name}_{ontology_code}, so for instance ncit_C123456

To update the _terms.yaml file we need to run dictionaryutils/bin/buklk_load_terms_file.py when we have a new all_variables.json version.



The dictionaryutils/bin/create_json.py script associate the enumeration values between the YAML files and the all_variables.json file adding in the created schema.json the reference between the YAML file definition and the terminology saved in the _terms.yaml file.

So for instance this is a variable in a YAML file: 
```
  cimt_type:
    description: "Cellular Immunotherapy Type"
    enum:
      - Donor Lymphocyte Infusion
      - Chimeric Antigen Receptor T-cell Therapy
      - Other
      - Unknown
      - Not Reported
```

This is the variable definition in the all_variables.json file
```
"values": {
            "Chimeric Antigen Receptor T-cell Therapy": {
                "sources": [
                    "Aggregated",
                    "AML",
                    "HL"
                ],
                "codes": [
                    "ncit:C126102"
                ],
                "descriptions": {
                    "Treatment that uses T-cells that have been engineered to contain a chimeric antigen receptor (CAR) that specifically targets a particular antigen.": [
                        "Aggregated",
                        "AML",
                        "HL"
                    ]
                },
                "inotes": {}
            },
            "Donor Lymphocyte Infusion": {
                "sources": [
                    "Aggregated",
                    "AML",
                    "HL"
                ],
                "codes": [
                    "ncit:C16145"
                ],
                "descriptions": {
                    "The infusion of donor lymphocytes following hematopoietic stem cell transplantation for the purpose of augmenting the host immune response or preventing the rejection of the graft.": [
                        "Aggregated",
                        "AML",
                        "HL"
                    ]
                },
                "inotes": {}
            },
            "Other": {
                "sources": [
                    "Aggregated",
                    "AML",
                    "HL"
                ],
                "codes": [
                    "ncit:C17649",
                    ""
                ],
                "descriptions": {
                    "Different than the one(s) previously specified or mentioned.": [
                        "Aggregated",
                        "AML",
                        "HL"
                    ]
                },
                "inotes": {}
            },
            "Unknown": {
                "sources": [
                    "Aggregated",
                    "AML",
                    "HL"
                ],
                "codes": [
                    "ncit:C17998"
                ],
                "descriptions": {
                    "Reported as unknown by the data contributor.": [
                        "Aggregated",
                        "AML",
                        "HL"
                    ]
                },
                "inotes": {}
            },
            "Not Reported": {
                "sources": [
                    "Aggregated",
                    "AML",
                    "HL"
                ],
                "codes": [
                    "ncit:C43234"
                ],
                "descriptions": {
                    "Not provided or available.": [
                        "Aggregated",
                        "AML",
                        "HL"
                    ]
                },
                "inotes": {}
            }
        }
```

This is the generated variables in the _terms.yaml file:
```
ncit_C126102:
  description: Treatment that uses T-cells that have been engineered to contain a
    chimeric antigen receptor (CAR) that specifically targets a particular antigen.
  termDef:
    cde_id: C126102
    cde_version: Version:23.02d (Release date:2023-02-27)
    source: ncit
    term: Chimeric Antigen Receptor T-Cell Therapy
    term_url: https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C126102
ncit_C16145:
  description: The infusion of donor lymphocytes following hematopoietic stem cell
    transplantation for the purpose of augmenting the host immune response or preventing
    the rejection of the graft.
  termDef:
    cde_id: C16145
    cde_version: Version:23.02d (Release date:2023-02-27)
    source: ncit
    term: Donor Lymphocyte Infusion
    term_url: https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C16145
ncit_C17649:
  description: Different than the one(s) previously specified or mentioned.
  termDef:
    cde_id: C17649
    cde_version: Version:23.02d (Release date:2023-02-27)
    source: ncit
    term: Other
    term_url: https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17649
ncit_C17998:
  description: Not known, observed, recorded; or reported as unknown by the data contributor.
  termDef:
    cde_id: C17998
    cde_version: Version:23.02d (Release date:2023-02-27)
    source: ncit
    term: Unknown
    term_url: https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998
ncit_C43234:
  description: Not provided or available.
  termDef:
    cde_id: C43234
    cde_version: Version:23.02d (Release date:2023-02-27)
    source: ncit
    term: Not Reported
    term_url: https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234
```

And this is the generated schema:
```

"cimt_type":
            {
                "description": "Cellular Immunotherapy Type",
                "enum":
                [
                    "Donor Lymphocyte Infusion",
                    "Chimeric Antigen Receptor T-cell Therapy",
                    "Other",
                    "Unknown",
                    "Not Reported"
                ],
                "term":
                [
                    {
                        "$ref": "_terms.yaml#/ncit_C173289"
                    }
                ],
                "enumDef":
                [
                    {
                        "$ref": "_terms.yaml#/ncit_C126102",
                        "enumeration": "Chimeric Antigen Receptor T-cell Therapy"
                    },
                    {
                        "$ref": "_terms.yaml#/ncit_C16145",
                        "enumeration": "Donor Lymphocyte Infusion"
                    },
                    {
                        "$ref": "_terms.yaml#/ncit_C17649",
                        "enumeration": "Other"
                    },
                    {
                        "$ref": "_terms.yaml#/ncit_C17998",
                        "enumeration": "Unknown"
                    },
                    {
                        "$ref": "_terms.yaml#/ncit_C43234",
                        "enumeration": "Not Reported"
                    }
                ]
            },
```
