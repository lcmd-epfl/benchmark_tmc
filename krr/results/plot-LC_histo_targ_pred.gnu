#!/usr/bin/gnuplot
reset
set terminal svg size 1300,900 enhanced
set output "targets_preds-histograms-per_split.svg"

set macros
binwidth = 0.1
binstart = -(binwidth/2)

transparency = 0.5
set style fill transparent solid transparency noborder # partial transparency
set boxwidth 0.9*binwidth absolute


set ls 1 lc 'red' lt 1
set ls 2 lc 'blue' lt 1
set ls 3 lc 'yellow' lt 1

#stats "< paste ".FILES u 1
#set title "Mean = ".sprintf("%.2f",STATS_mean)." (+/- ".sprintf("%.2f",STATS_stddev).")" 

FILE="LC_SPAHM_e-TM-GSspinPlus.npy_splitting-TM-GSspinPlus.txt_predictions.txt"	

MAES="103.377 108.366 33.3931 124.465 107.062 33.9579 104.375 106.317 114.461 111.257"

set multiplot layout 2,5  title ""

do for [i=1:19:2]{
	j=i+1

	set title "MAE = ".word(MAES, j/2)

	set ylabel 'Count'
	set xlabel 'Spin-splitting energy / eV x10^2'

	#set format x "%e"

	if (i==1){
		set key at screen 0.6,0.95 maxrows 1 offset 0,2
	}
	else {
		unset key
	}
	
	plot FILE u (binwidth*(floor(((column(i)/100)-binstart)/binwidth)+0.5)+binstart):(1.0) \
		smooth freq w boxes \
		lc "blue" fs transparent solid transparency t "Targets", \
		"" u (binwidth*(floor(((column(j)/100)-binstart)/binwidth)+0.5)+binstart):(1.0) \
		smooth freq w boxes \
		lc "red" fs transparent solid transparency t "Predictions"
	
}
