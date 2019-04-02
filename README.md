# Ransomware machine learning project

## Malware dataset

### VirusShare

We used the `VirusShare_CryptoRansom_20160715.zip` malware collection from *VirusShare.com*.

### Meta information

The information were collected via the *VirusTotal.com* academic API.

### Labels

The labels are created based on the meta information collected from *VirusTotal.com* by the *avclass* (<https://github.com/malicialab/avclass)> tool.

We modified the tool that it can handle the `json` academic API reports of *VirusTotal.com*.

### Clean

To clean the `json` reports from linebreaks (necessary for *avclass* to work):

```bash
#!/bin/bash
for filename in ./VTDL_VirusShare/*.json; do
    f="${filename##*/}"
    (tr '\n' ' '<$filename) >> ./VTDL_VirusShare_clean/$f
done
```

### Modification

Replace the method `get_sample_info` line 61 - 82 in `avclass_common.py` with:

```python
@staticmethod
def get_sample_info(vt_rep, from_vt):
    '''Parse and extract sample information from JSON line
        Returns a SampleInfo named tuple: md5, sha1, sha256, label_pairs
    '''
    label_pairs = []
    if from_vt:
        try:
            scans = vt_rep['data']['attributes']['last_analysis_results']
        except KeyError:
            return None
        for av, res in scans.items():
            if res['category'] == 'malicious':
                label = res['result']
                clean_label = filter(lambda x: x in string.printable,
                                    label).strip().encode('utf-8').strip()
                label_pairs.append((av, clean_label))
    else:
        label_pairs = vt_rep['av_labels']

    return SampleInfo(vt_rep['data']['attributes']['md5'], vt_rep['data']['attributes']['sha1'], vt_rep['data']['attributes']['sha256'],
                           label_pairs)
```

## Generators

### Install

``pip install -r requirements.txt``

### Usage

#### Image

Creates random images of type jpg and png.\
``ìmage.py <width> <height> <number_of_images>``

#### PDF

Downloads 100 pdfs of random article from wikipedia.\
``pdf.py``

#### Word

Creates random word documents.\
``word.py <number_of_documents>``

#### ZIP

Zips all files in the same folder.\
``zip.py``

#### Wikimedia

Downloads media (random or category) from Wikimedia.\
``wikimedia.py <random|category> <number of random files|wikimedia category>``

## References

* Kharraz, Amin, et al. "Cutting the gordian knot: A look under the hood of ransomware attacks." International Conference on Detection of Intrusions and Malware, and Vulnerability Assessment. Springer, Cham, 2015.
* Kharaz, Amin, et al. "{UNVEIL}: A Large-Scale, Automated Approach to Detecting Ransomware." 25th {USENIX} Security Symposium ({USENIX} Security 16). 2016.
* Kharraz, Amin, and Engin Kirda. "Redemption: Real-time protection against ransomware at end-hosts." International Symposium on Research in Attacks, Intrusions, and Defenses. Springer, Cham, 2017.
* Kharraz, Amin, William Robertson, and Engin Kirda. "Protecting against Ransomware: A New Line of Research or Restating Classic Ideas?." IEEE Security & Privacy 16.3 (2018): 103-107.
* Scaife, Nolen, et al. "Cryptolock (and drop it): stopping ransomware attacks on user data." 2016 IEEE 36th International Conference on Distributed Computing Systems (ICDCS). IEEE, 2016.
* Continella, Andrea, et al. "ShieldFS: a self-healing, ransomware-aware filesystem." Proceedings of the 32nd Annual Conference on Computer Security Applications. ACM, 2016.
* Held, Matthias, and Marcel Waldvogel. "Fighting Ransomware with Guided Undo." Proceedings of the 11th Norwegian Information Security Conference. 2018.
* Takeuchi, Yuki, Kazuya Sakai, and Satoshi Fukumoto. "Detecting ransomware using support vector machines." Proceedings of the 47th International Conference on Parallel Processing Companion. ACM, 2018.