import numpy as np
import os, sys
sys.path.append("../")
from latex_array import latex_array

x = [
	[1.321, 2.123, 3.43, 4.000, 5.12],
	[6, 7.32, 8.351, 9.12, 0.3254],
	[-1.321, -2.124, -3.321]
]

# normal
latex_array('latex_array_results/latex_array_test_normal.res', x)

# single transposed
latex_array('latex_array_results/latex_array_test_transpose_single.res', np.linspace(0, 10, 10), transpose_single="True")

# padding
latex_array('latex_array_results/latex_array_test_padding.res', x, padding=True, padding_char="#")

# transposing
latex_array('latex_array_results/latex_array_test_transpose.res', x, transpose=True)


x = [	[1.321, 2.123, 3.43, 4.000, 5.12],
	[6, 7.32, 8.351, 9.12, 0.3254],
	[-1.321, -2.924, -3.321, -4.12342, -5.90843] ]
# format single
format = "{:.4f}"
latex_array('latex_array_results/latex_array_test_format_single.res', x, format=format)

# format row
format = ["{:.0f}", "{:.4f}", "{:.4f}", "{:.4f}", "{:.4f}"]
latex_array('latex_array_results/latex_array_test_format_line.res', x, format=format)

# format column
format = ["{:.0f}", "{:.4f}", "{:.4f}"]
latex_array('latex_array_results/latex_array_test_format_column.res', x, format=format)

# format array
format = [	["{:.0f}", "{:.4f}", "{:.4f}", "{:.4f}", "{:.2f}"],
		["{:.4f}", "{:.0f}", "{:.4f}", "{:.1f}", "{:.4f}"],
		["{:.4f}", "{:.4f}", "{:.0f}", "{:.4f}", "{:.4f}"] ]
latex_array('latex_array_results/latex_array_test_format_array.res', x, format=format)

# np.array in list
x = [np.linspace(0, 10, 5), np.arange(0, 10, 1), np.linspace(-5, 5, 11)]
latex_array('latex_array_results/latex_array_test_np_array.res', x, transpose=True)
