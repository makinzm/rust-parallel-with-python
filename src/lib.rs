use pyo3::prelude::*;
use pyo3_asyncio::tokio;
use tokio::time::{sleep, Duration};

#[pyfunction]
fn async_sleep(py: Python, seconds: u64) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        sleep(Duration::from_secs(seconds)).await;
        Ok(())
    })
}

#[pymodule]
fn rust_parallel_with_python(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(async_sleep, m)?)?;
    Ok(())
}

