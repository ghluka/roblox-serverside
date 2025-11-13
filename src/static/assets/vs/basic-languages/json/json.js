define(["require", "exports"], function (require, exports) {
    exports.conf = {
        comments: {
            lineComment: "//",
            blockComment: ["/*", "*/"]
        },

        brackets: [
            ["{", "}"],
            ["[", "]"]
        ],

        autoClosingPairs: [
            { open: "{", close: "}" },
            { open: "[", close: "]" },
            { open: "\"", close: "\"" }
        ],

        surroundingPairs: [
            { open: "{", close: "}" },
            { open: "[", close: "]" },
            { open: "\"", close: "\"" }
        ]
    };

    exports.language = {
        defaultToken: "",
        tokenPostfix: ".json",

        keywords: [
            "true", "false", "null"
        ],

        tokenizer: {
            root: [
                { include: "@whitespace" },

                [/"/, { token: "string.quote", next: "@string" }],

                [/-?\d+(\.\d+)?([eE][+-]?\d+)?/, "number"],

                [/[{}[\],:]/, "delimiter.bracket"],

                [/\b(?:true|false|null)\b/, "keyword"]
            ],

            whitespace: [
                [/[ \t\r\n]+/, ""],
                [/\/\/.*$/, "comment"],
                [/\/\*/, "comment", "@comment"]
            ],

            comment: [
                [/[^/*]+/, "comment"],
                [/\*\//, "comment", "@pop"],
                [/./, "comment"]
            ],

            string: [
                [/[^\\"]+/, "string"],
                [/\\./, "string.escape"],
                [/"/, { token: "string.quote", next: "@pop" }]
            ]
        }
    };
});
