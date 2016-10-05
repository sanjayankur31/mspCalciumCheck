set term pngcairo font "OpenSans, 28" size 1920,1028
set xlabel "Current (pA)"
set ylabel "Firing rate (Hz)"
set output "rate-vs-current.png"
set title "Firing rate vs input current for TIF neurons"
plot "calcium-data.txt" using 1:2 with lines lw 4 title "Firing rate"

set xlabel "Rate (Hz)"
set ylabel "Calcium concentration"
set output "calcium-vs-firing-rate.png"
set title "Calcium concentration vs firing rate for TIF neurons"
plot "calcium-data.txt" using 2:3 with lines lw 4 title "[Ca]"

set xlabel "Current (pA)"
set ylabel "Calcium concentration"
set output "calcium-vs-current.png"
set title "Calcium concentration vs input current for TIF neurons"
plot "calcium-data.txt" using 1:3 with lines lw 4 title "[Ca]"
