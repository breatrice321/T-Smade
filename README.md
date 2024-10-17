T-Smade: A Two-stage Smart Detector for Evasive Spectre Attacks Under Various Workloads
================================================================================================================
Introduction
------------
This project is designed to detect two evasive Spectre attacks (evasive Spectre nop and evasive Spectre memory) using the two-stage models trained with Spectre attack. <br>
The two-stage models include the first stage workloads classifier and the second stage attack detector. <br>
The workloads include three types: realistic applications (6 appliccations), CPU stress test and memory stress test. <br>
More indepth information can be found in the corresponding paper: https://www.mdpi.com/2079-9292/13/20/4090 <br>

Requirement
------------
python=3.8 <br>
event2 need to download a geckodriver and put it into noise file <br>
event6 need to run a command (below) in terminal before execute event6.py and use_event6.py <br>
/opt/libreoffice5.4/program/soffice.bin "--accept=socket,host=localhost,port=2002;urp; <br>

Cite it
------------
@Article{electronics13204090,
AUTHOR = {Jiao, Jiajia and Wen, Ran and Li, Yulian},
TITLE = {T-Smade: A Two-Stage Smart Detector for Evasive Spectre Attacks under Various Workloads},
JOURNAL = {Electronics},
VOLUME = {13},
YEAR = {2024},
NUMBER = {20},
ARTICLE-NUMBER = {4090},
ISSN = {2079-9292},
}
