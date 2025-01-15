import { assert, expect, test } from 'vitest';
import { getData } from './emoji.service';

test("fetch emoji text", async () => {
    let [text, err ] = await getData()
    if (err !== undefined){
        assert.isTrue(false, `error fetching data: ${err}`)
    }

    expect(text.length).greaterThan(0)
});
