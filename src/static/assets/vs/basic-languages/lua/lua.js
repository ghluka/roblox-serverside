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
        ],
        surroundingPairs: [
            { open: "{", close: "}" },
            { open: "[", close: "]" },
            { open: "(", close: ")" },
            { open: '"', close: '"' },
            { open: "'", close: "'" },
            { open: "`", close: "`" },
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
            "print", "error", "warn", "require", "game", "assert",
            "rawset", "rawget", "rawequal",
            "coroutine", "debug", "table", "pairs", "ipairs", "bit", "bit32", "math", "utf8", "os",
            "collectgarbage", "getfenv", "getmetatable",
            "loadfile", "loadstring", "newproxy", "next",
            "pcall", "select", "setfenv",
            "setmetatable", "tonumber", "tostring", "type", "xpcall", "_G",
            "shared", "delay", "spawn", "tick", "typeof", "wait",
            "Enum", "script", "workspace", "printidentity",
        ],

        typeKeywords: [
            "number", "string", "boolean", "nil", "any", "unknown",
            "thread", "userdata", "table", "function", "never",
            "Axes", "BrickColor", "CatalogSearchParams", "CFrame", "Color3", "ColorSequence",
            "ColorSequenceKeypoint", "DateTime", "Drawing", "DockWidgetPluginGuiInfo", "Faces",
            "Instance", "NumberRange", "NumberSequence", "NumberSequenceKeypoint", "PathWaypoint",
            "PhysicalProperties", "Random", "Ray", "RaycastParams", "RaycastResult", "Rect",
            "Region3", "Region3int16", "TweenInfo", "UDim", "UDim2", "Vector2", "Vector2int16",
            "Vector3", "Vector3int16",
			
            "any", "boolean", "number", "string", "table", "thread", "userdata",
        ],

        operators: [
            "+", "-", "*", "/", "%", "^", "#", "==", "~=", "<=", ">=", "<", ">",
            "=", ";", ":", ".", "..", ",", "(", ")", "{", "}", "[", "]",
        ],

        symbols: /[=><!?:&|+\-*\/\^%#]+/,
        escapes: /\\(?:[abfnrtv\\"'`]|x[0-9A-Fa-f]{2}|u\{[0-9A-Fa-f]+\})/,

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

                [/0[xX][0-9A-Fa-f_]*[0-9A-Fa-f]/, "number.hex"],
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
