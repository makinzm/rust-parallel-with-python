use pyo3::prelude::*;
use std::thread;
use std::sync::{Arc, Mutex};

// Rustから呼び出される関数。並列に処理を行う。
#[pyfunction]
fn parallel_computation(n: usize) -> PyResult<Vec<usize>> {
    let results = Arc::new(Mutex::new(vec![0; n]));
    let mut handles = vec![];

    for i in 0..n {
        let results = Arc::clone(&results);
        let handle = thread::spawn(move || {
            let mut data = results.lock().unwrap();
            data[i] = i * i; // 例として、インデックスの二乗を計算
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    let results = Arc::try_unwrap(results).unwrap().into_inner().unwrap();
    Ok(results)
}

/// Pythonモジュールとして公開
#[pymodule]
fn my_parallel_project(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parallel_computation, m)?)?;
    Ok(())
}

