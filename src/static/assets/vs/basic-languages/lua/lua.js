/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
/*
	Modified by Nett.WTF to support LuaU syntax.
*/
define(["require", "exports"], function (require, exports) {
    exports.conf = {
        comments: {
            lineComment: "--",
            blockComment: ["--[[", "]]"],
        },
        brackets: [
            ["{", "}"],
            ["[", "]"],
            ["(", ")"],
        ],
        autoClosingPairs: [
            { open: "{", close: "}" },
            { open: "[", close: "]" },
            { open: "(", close: ")" },
            { open: '"', close: '"', notIn: ["string"] },
            { open: "'", close: "'", notIn: ["string"] },
            { open: "`", close: "`", notIn: ["string"] },
            { open: "[[", close: "]]", notIn: ["string"] },
        ],
        surroundingPairs: [
            { open: "{", close: "}" },
            { open: "[", close: "]" },
            { open: "(", close: ")" },
            { open: '"', close: '"' },
            { open: "'", close: "'" },
            { open: "`", close: "`" },
            { open: "[[", close: "]]" },
        ],
    };

    exports.language = {
        defaultToken: "",
        tokenPostfix: ".luau",

        keywords: [
            "and", "break", "do", "else", "elseif", "end", "false", "for", "function",
            "goto", "if", "in", "local", "nil", "not", "or", "repeat", "return",
            "then", "true", "until", "while", "continue",
        ],

        builtins: [
            "print", "warn", "error", "assert", "pcall", "xpcall", "type", "next",
            "pairs", "ipairs", "select", "tonumber", "tostring", "unpack",
            "math", "string", "table", "coroutine", "os", "debug", "game",
            "workspace", "script", "Instance", "Vector3", "CFrame", "UDim2",
        ],

        typeKeywords: [
            "any", "boolean", "number", "string", "table", "thread", "userdata",
        ],

        operators: [
            "+", "-", "*", "/", "%", "^", "#", "==", "~=", "<=", ">=", "<", ">",
            "=", ";", ":", ".", "..", ",", "(", ")", "{", "}", "[", "]",
        ],

        symbols: /[=><!~?:&|+\-*\/\^%#]+/,
        escapes: /\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{2}|u\{[0-9A-Fa-f]+\})/,

        tokenizer: {
            root: [
                [/[a-zA-Z_]\w*/, {
                    cases: {
                        "@keywords": "keyword",
                        "@builtins": "type.identifier",
                        "@typeKeywords": "type",
                        "@default": "identifier",
                    },
                }],

                { include: "@whitespace" },

                [/\d*\.\d+([eE][\-+]?\d+)?/, "number.float"],
                [/\d+/, "number"],

                [/"([^"\\]|\\.)*$/, "string.invalid"],
                [/'([^'\\]|\\.)*$/, "string.invalid"],
                [/"/, "string", "@string_double"],
                [/'/, "string", "@string_single"],

                [/\[=*\[/, { token: "string", next: "@multiString" }],

                [/`/, { token: "string.quote", next: "@templateString" }],

                [/@symbols/, {
                    cases: {
                        "@operators": "operator",
                        "@default": "",
                    },
                }],

                [/[{}()\[\]]/, "@brackets"],
                [/[;,.:]/, "delimiter"],
            ],

            whitespace: [
                [/[ \t\r\n]+/, ""],
                [/--\[=*\[/, "comment", "@commentBlock"],
                [/--.*$/, "comment"],
            ],

            string_double: [
                [/[^\\"]+/, "string"],
                [/@escapes/, "string.escape"],
                [/\\./, "string.escape.invalid"],
                [/"/, "string", "@pop"],
            ],

            string_single: [
                [/[^\\']+/, "string"],
                [/@escapes/, "string.escape"],
                [/\\./, "string.escape.invalid"],
                [/'/, "string", "@pop"],
            ],

            multiString: [
                [/\]=*\]/, { token: "string", next: "@pop" }],
                [/./, "string"],
            ],

            commentBlock: [
                [/\]=*\]/, { token: "comment", next: "@pop" }],
                [/./, "comment"],
            ],

            templateString: [
                [/[^\\`{]+/, "string"],
                [/\\./, "string.escape"],
                [/\{/, { token: "delimiter.bracket", next: "@templateExpression" }],
                [/`/, { token: "string.quote", next: "@pop" }],
            ],

            templateExpression: [
                [/\{/, { token: "delimiter.bracket", next: "@templateExpression" }],
                [/\}/, { token: "delimiter.bracket", next: "@pop" }],
                { include: "root" },
            ],
        },
    };
});
