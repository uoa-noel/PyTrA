from pymc import *
from traits.api import  HasTraits, File, Button, Array, Enum, Instance, Str, List, HasPrivateTraits, Float, Int
from traitsui.api import Group, Item, View, Label, HSplit, Tabbed, ListEditor
from Data import Data

class MCMC(HasTraits):
    parameters = List
    iter = Int(10000)
    burn_in = Int(0)
    run = Button("Run")
    prior_dict = dict()

    view = View(
        Item( 'parameters',
            style  = 'custom',
            editor = ListEditor( use_notebook = True,
                deletable    = True,
                dock_style   = 'tab',
                page_name    = '.name' )
        ),

        Item('iter'),
        Item('burn_in'),
        Item('run'),
        Label('See log file for ouput'),
        title   = 'MCMC', resizable=True,
        buttons = [ 'OK', 'Cancel' ]
    )

    def _Run_fired(self):

        for i in range(len(self.parameters)):

            #Sets a Poisson Distribution
            if self.parameters[i].dist=='Poisson':
                self.prior_dict[self.parameters[i]]=0

            #Sets a Normal Distribution
            if self.parameters[i].dist=='Normal':
                self.prior_dict[self.parameters[i]]=self.parameters[i].min,self.parameters[i].max

            #Sets a Uniform Distribution
            if self.parameter[i].dist=='Uniform':
                self.prior_dict[self.parameters[i]]=self.parameters[i].min

        print "dictionary created"
        print self.parameters

        try:
            model = Data.tracefitmodel.getMCMC(priors=self.prior_dict)
        except:
            print 'error'

        model.sample(self.iter,burn=self.burn_in)

        Matplot.plot(model)
        plt.show()

class Params(HasPrivateTraits):
    #Name of string
    i = Int
    name = Str
    min = Float
    max = Float
    sig = Float
    dist = Enum('Normal','Uniform','Poisson')

    view = View(
        Item('name',label='Parameter name',style='readonly'),
        Item('min',label='Lower value for Uniform'),
        Item('max',label='Upper value for Uniform'),
        Item('sig',label='Sigma value for Normal'),
        Item('dist',label='Distribution for parameter'),
    )