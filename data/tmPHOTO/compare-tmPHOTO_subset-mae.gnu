#!/usr/bin/env gnuplot

set terminal svg size 900,600 noenhanced
set output "tmPHOTO_subset-mae.svg"

set boxwidth 0.9 relative
set style data histograms

#set errorbars fullwidth
set style fill solid 1.0 border lt -1
set style histogram gap 2 

keys="tmQMg_ref-test_mae	65%_tmPHOTO-test_mae 	100%_tmPHOTO_3dmol-ref       	train_mae	val_mae"

set ls 1 lc 'royalblue' lt 1
set ls 2 lc 'light-red' lt 1

set ylabel "MAE"
set xlabel "Targets"

set title "Comparison of uNatQG model to our results (mixed sub- and full tmPHOTO dataset)"
set ytics 0.5
set format y "%.2f"
plot for [i=2:4:1] "./tmPHOTO_subset-mae.dat" u i:xticlabels(1) ls i t word(keys, i-1)
