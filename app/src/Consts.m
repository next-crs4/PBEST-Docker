classdef Consts
    properties( Constant = true )
      script_name = "pbest"
      version = "0.1"
      short_desc = "identify asymptomatic COVID-19 carriers"
      long_desc = "Used to screen COVID-19 samples via group testing, as described in the manuscript (by Shental et al)\n\"Efficient high throughput SARS-CoV-2 testing to detect asymptomatic carriers\".\nThe protocol allows screening 384 samples using 48 pools, \nwhere each sample appears in six pools according to a Reed-Solomon error-correcting code."
      pool_matrix ="/app/files/poolingMatrix"
    end

end