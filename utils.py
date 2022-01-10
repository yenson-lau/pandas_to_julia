import pyarrow as pa

def df_to_arrowbytes(df):
    batch = pa.record_batch(df)
    sink = pa.BufferOutputStream()

    with pa.ipc.new_stream(sink, batch.schema) as writer:
        writer.write_batch(batch)

    return bytearray(sink.getvalue().to_pybytes())


def arrowbytes_to_df(arrowbytes):
    return pa.ipc.open_stream(arrowbytes).read_pandas()
