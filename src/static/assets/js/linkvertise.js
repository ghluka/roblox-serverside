const LINKVERTISE_PUBLIC_KEY =
    "-----BEGIN PUBLIC KEY-----\n" +
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1piHDY9WRIehbfC3Fpol\n" +
    "Ly/WrJF8TKFVdDMobj3fkNjN/69dTv9JgXt+gcJxVn/h4NCMtQ2mCQXNBMXzLOky\n" +
    "HJipiFMoyPtOOlMlbWRAiaQE1GpMebGNRcsxYnWzF53v63+hUQgrMahH9X0Ii/NJ\n" +
    "hvDyFlPX77+z9xiyd45L+xrgayePpOxvQpj6VJDlpNNKWbuIkFvkMmUVRM2TLulL\n" +
    "JSgs4EgoBZgTYRpmhgR8tYfDOW+cOctffggcMAzKUC2CzYNmhzX15O7DKaZdYgfa\n" +
    "BR/hqvyNAxBepHOJnBfHkQqaox5diHGqdwXXLwiJKzoK5R26vaI3jg2+d69VPSGL\n" +
    "0QIDAQAB\n" +
    "-----END PUBLIC KEY-----";

function _str2ab(str) {
    const buf = new ArrayBuffer(str.length);
    const view = new Uint8Array(buf);
    for (let i = 0; i < str.length; i++) view[i] = str.charCodeAt(i);
    return buf;
}

let _importedKey = null;
async function _getKey() {
    if (_importedKey) return _importedKey;
    const body = LINKVERTISE_PUBLIC_KEY
        .replace("-----BEGIN PUBLIC KEY-----", "")
        .replace("-----END PUBLIC KEY-----", "")
        .replace(/\s+/g, "");
    _importedKey = await window.crypto.subtle.importKey(
        "spki",
        _str2ab(window.atob(body)),
        { name: "RSA-OAEP", hash: { name: "SHA-256" } },
        true,
        ["encrypt"]
    );
    return _importedKey;
}

async function linkvertiseLink(publisherId, targetUrl) {
    const key = await _getKey();

    const chars = [...decodeURI(targetUrl)];
    const encoder = new TextEncoder();
    const bytes = [];
    let ch = chars.shift();
    while (ch != null) {
        bytes.push(...encoder.encode(ch));
        if (bytes.length > 66) break;
        ch = chars.shift();
    }
    const remainder = chars.join("");

    const encrypted = await window.crypto.subtle.encrypt(
        { name: "RSA-OAEP", hash: { name: "SHA-256" } },
        key,
        new Uint8Array(bytes)
    );

    let raw = "";
    const encBytes = new Uint8Array(encrypted);
    for (let i = 0; i < encBytes.byteLength; i++) {
        raw += String.fromCharCode(encBytes[i]);
    }

    const r = btoa(raw) + remainder;
    const base =
        "https://link-to.net/" + publisherId + "/" + Math.random() * 1000 + "/dynamic/";
    return encodeURI(base + "?r=" + r + "&v=2");
}

window.linkvertiseLink = linkvertiseLink;
