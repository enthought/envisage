To build the AcmeLab example:-

    cd .../src/acme.acmelab
    python setup.py sdist --dist-dir ../../dist/eggs

    cd .../src/acme.workbench
    python setup.py bdist_egg --dist-dir ../../dist/eggs

    cd ../../dist/eggs
    unzip the acmelab zip file
    add a '.egg' extension to each unzipped folder

Surely there must be a better way to do this? I'm not an egg expert!

To run the example:-

     cd .../envisage.ui.workbench_3.0/examples/AcmeLab/dist
     python run.py

