use pyo3::prelude::*;
use pyo3_asyncio::tokio::future_into_py;
use tokio::time::{sleep, Duration};

/// 非同期に指定された秒数待機する関数
#[pyfunction]
fn async_sleep(py: Python, secs: u64) -> PyResult<&PyAny> {
    future_into_py(py, async move {
        sleep(Duration::from_secs(secs)).await;
        Ok(())
    })
}

/// Pythonモジュールとして公開する
#[pymodule]
fn my_rust_extension(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(async_sleep, m)?)?;
    Ok(())
}

