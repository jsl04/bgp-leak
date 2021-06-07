# -*- mode: python; python-indent: 4 -*-
import ncs
import string
from ncs.application import Service



# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):
    
    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        # starting with empty value
        val = ''
        # looping the list of destinations
        for dest in service.prefix_import:
            # adding if-statement per each destination
            val += ('  if destination in '
                    + '('
                    + str(dest.prefix_set)
                    + ')'
                    + 'and\n'
                    + '\n    extcommunity rt matches-any '
                    + '('
                    + str(1)
                    + ':'
                    + str(69)
                    + ')'
                    + 'then\n'
                    + '\n  done\n')
        val += '  endif\n'
        vars = ncs.template.Variables()
        vars.add('VAL', val)
        template = ncs.template.Template(service)
        template.apply('bgp-leak-template', vars)


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('bgp-leak-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
