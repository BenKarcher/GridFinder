use std::collections::HashSet;

use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn find(encoded_lines: Vec<Vec<usize>>, max: i32) -> PyResult<Vec<Vec<usize>>> {
    let width = encoded_lines[0].len();

    let mut prefixes = Vec::new();
    for i in 0..width {
        prefixes.push(HashSet::new());
        for row in &encoded_lines {
            prefixes[i].insert(row[0..=i].iter().fold(0, |acc, x| acc * (width + 1) + x));
        }
    }

    let mut result = Vec::new();

    let mut state = vec![0; width * width];
    let mut remaining = max;
    for line in &encoded_lines {
        copyInto(&mut state, &line, width, 0);
        find_rec(
            &mut state,
            1,
            width,
            &encoded_lines,
            &prefixes,
            &mut remaining,
            &mut result,
        );
        if remaining <= 0 {
            break;
        }
    }
    Ok(result)
}

fn copyInto(state: &mut Vec<usize>, line: &Vec<usize>, width: usize, row: usize) {
    for i in 0..width {
        state[i + row * width] = line[i];
    }
}

fn find_rec(
    state: &mut Vec<usize>,
    height: usize,
    width: usize,
    encoded_lines: &Vec<Vec<usize>>,
    prefixes: &Vec<HashSet<usize>>,
    max: &mut i32,
    result: &mut Vec<Vec<usize>>,
) {
    let prefix = &prefixes[height];
    let mut remaining = max;

    for line in encoded_lines {
        copyInto(state, line, width, height);
        if (0..width).all(|col| {
            prefix.contains(
                &state
                    .iter()
                    .skip(col)
                    .step_by(width)
                    .take(height + 1)
                    .fold(0, |acc, x| acc * (width + 1) + x),
            )
        }) {
            if height + 1 == width {
                result.push(state.clone());
                *remaining -= 1;
            } else {
                find_rec(
                    state,
                    height + 1,
                    width,
                    encoded_lines,
                    prefixes,
                    remaining,
                    result,
                );
            }
            if *remaining <= 0 {
                break;
            }
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn latinFinder(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find, m)?)?;
    Ok(())
}
