"""
"""

from bbtest import WindowsHost, LinuxHost, LocalHost, Windows64Host
from bbtest import BBTestCase

from cybereason.boxes.servers import TransparencyBox, RegistrationBox, PerspectiveBox, PersonalizationBox, ArtifactoryBox
from cybereason.boxes.sensor import SensorBox
from cybereason.services.abstracted import SensorPolicy

from cybereason.services.ecosystem import logger


class CRTestCase(BBTestCase):
    pass


class InstallTest(CRTestCase):

    LAB = {
        'endpoint': {
            'class': Windows64Host,
            'boxes': [],
         },
        'repository': {
            'class': LinuxHost,
            'boxes': [],
         },
        'perspective': {
            'class': LinuxHost,
            'boxes': [PerspectiveBox],
         },
        'transparency': {
            'class': LinuxHost,
            'boxes': [TransparencyBox],
         },
        'registration': {
            'class': LinuxHost,
            'boxes': [RegistrationBox],
         },
        'download': {
            'class': LinuxHost,
            'boxes': [ArtifactoryBox],
        },
        'local': {
            'class': LocalHost,
            'boxes': [PersonalizationBox],
        }
    }

    address_book = {
        'perspective':
            {'ip': '3.86.19.247', 'username': 'admin@cybereason.com', 'password': 'jPUoWCg8Pok='},
        'transparency':
            {'ip': '3.85.179.129'},
    }

    # FFU

    RLAB = {
        'hosts': {'endpoint': {'class': WindowsHost}},
        'boxes': [PerspectiveBox,
                  TransparencyBox,
                  RegistrationBox,
                  PersonalizationBox,
                  10*[SensorBox]]
    }

    raddress_book = {
        PerspectiveBox:
            {'ip': '3.86.19.247', 'username': 'admin@cybereason.com', 'password': 'jPUoWCg8Pok='}
    }

    # End FFU

    def test_install(self):
        perspective_host = self.lab.hosts['perspective']
        logger.info(f'perspective_host.ip = {perspective_host.ip}')
        perspective = self.lab.boxes[PerspectiveBox.NAME][0]
        logger.info(f'perspective.host.ip = {perspective.host.ip}')

        transparency = self.lab.boxes[TransparencyBox.NAME][0]
        endpoint = self.lab.hosts['endpoint']

        # CYBR-15877 - Add SensorPolicy configuration to SensorPolicy BB to allow Sensor Policy configurations

        sensor_policy = SensorPolicy(server=transparency)
        self.assertRaises(NotImplementedError, sensor_policy.config, None)

        sensor_policy = SensorPolicy(server=perspective)
        sensor_policy.config(None)

        # CYBR-15879 - Add Proxy configuration to Proxy BB to allow Proxy configurations.

        # CYBR-15883 - Add to Personaliztion BB the functionality to Download package from Packages Server and Personalize it

        personalization = self.lab.boxes[PersonalizationBox.NAME][0]
        artifactory = self.lab.boxes[ArtifactoryBox.NAME][0]
        package_downloaded, personalizer_downloaded = personalization.download(artifactory, 'rc-18.1.40', endpoint)
        assert personalization.host.isfile(package_downloaded)
        assert personalization.host.isfile(personalizer_downloaded)

        personalization.personalize(package_downloaded, personalizer_downloaded, transparency)

        # CYBR-15886 - Add functionality to Endpoint Host to download package from the Personalization server

        sensor = SensorBox(endpoint)
        sensor.download(personalization)
        sensor.install_wo_download()
