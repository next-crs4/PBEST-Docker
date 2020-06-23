#! /usr/bin/octave -qf

clear;
warning("off");
pkg load io;

function [] = printHelp()
    printf("# %s %s - %s #\n", Consts.script_name, Consts.version, Consts.short_desc);
    printf("\n%s\n", Consts.long_desc)
    printf("\nUsage:\n");
    printf("\t%s FILE.xlsx\n", Consts.script_name)
    printf("\n\tFILE.xlsx: 48x2")
end

Consts();

args = argv();
if size(args) ~= 1
    printHelp();
else
    exp_data = args{1};
    samples = main(exp_data);
    fprintf('\nDetected samples:\n')
    samples = samples.';
    disp(samples);
end



