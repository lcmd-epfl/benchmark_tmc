#!/usr/bin/gnuplot
reset
set terminal svg size 1300,900 noenhanced
set output "parity_plots-SPAHM_e-splitting-TM-GSspinPlus.svg"

set xlabel 'Targets'
set ylabel 'Predictions'

f(x)=x

set style fill transparent solid 0.25 # partial transparency
set style fill noborder # no separate top/bottom lines

set multiplot layout 2,5 title "Parity plots per random split i"

do for [i=1:19:2]{
	j=i+1
	FILE="LC_SPAHM_e-TM-GSspinPlus.npy_splitting-TM-GSspinPlus.txt_predictions.txt"	
	stats FILE u i:j nooutput
	SLOPES=STATS_slope
	ORIGINS=STATS_intercept
	lin(x,a,b)= a*x + b
	
	set title "i = ".sprintf("%d", (i+1)/2)." (R^2=".sprintf("%.2f",(STATS_correlation**2)).")"

	if (STATS_max_x > STATS_max_y) {MAX=STATS_max_x}
	else {MAX=STATS_max_y}
	if (STATS_min_x > STATS_min_y) {MIN=STATS_min_x}
	else {MIN=STATS_min_y}
	#set label 1 "(R^2=".sprintf("%.2f",(STATS_correlation**2)).")"  at graph 0.10,0.90
	set xrange [MIN:MAX]
	set yrange [MIN:MAX]
	
	set key outside top center offset -2,-2.5
	#set title FILES
	
	plot FILE u i:j w p ls i pt 5 noti, \
	f(x) w l ls 5 lc 'black' lw 1.5 noti,\
	lin(x,SLOPES, ORIGINS) w l ls i lw 1.5 dt 3 ti "Linear fit"
}
