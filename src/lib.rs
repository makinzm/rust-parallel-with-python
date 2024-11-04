use pyo3::prelude::*;
use std::thread;
use std::sync::{Arc, Mutex};

// Rustから呼び出される関数。並列に処理を行う。
#[pyfunction]
fn parallel_computation(n: usize) -> PyResult<Vec<usize>> {
    let results = Arc::new(Mutex::new(vec![0; n]));
    let mut handles = vec![];

    // nが非常に大きい場合、スレッドが大量に立ち上がる可能性がある
    // これはシステムのリソースを圧迫し、オーバーヘッドが大きくなる問題を引き起こす可能性があります。
    for i in 0..n {
        let results = Arc::clone(&results);
        let handle = thread::spawn(move || {
            let mut data = results.lock().unwrap();
            // lockの取得が複数スレッド間で競合する可能性があるため、
            // 実際のパフォーマンスが低下する可能性がある。
            // スレッド間で頻繁に共有データを書き換える必要がある場合、Mutexはボトルネックになることがあります。
            data[i] = i * i; // 例として、インデックスの二乗を計算
        });
        handles.push(handle);
    }

    // 各スレッドの終了を待機する
    for handle in handles {
        handle.join().unwrap(); // スレッドが正しく終了することを確認
    }

    // Arcの解除: ここでtry_unwrapを使ってArcを解放し、Mutex内部のデータにアクセスしています。
    // Arcが複数の参照でクローンされている場合、unwrapに失敗する可能性があります。
    let results = Arc::try_unwrap(results).unwrap().into_inner().unwrap();
    Ok(results)
}

/// Pythonモジュールとして公開
#[pymodule]
fn rust_parallel_with_python(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parallel_computation, m)?)?;
    Ok(())
}

