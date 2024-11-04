use pyo3::prelude::*;
use rayon::prelude::*; // Rayonを利用する

#[pyfunction]
fn parallel_computation(n: usize) -> PyResult<Vec<usize>> {
    let results: Vec<usize> = (0..n).into_par_iter() // Rayonによる並列イテレーション
        .map(|i| i * i) // インデックスの二乗を計算
        .collect();
    Ok(results)
}

#[pymodule]
fn rust_parallel_with_python(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parallel_computation, m)?)?;
    Ok(())
}

