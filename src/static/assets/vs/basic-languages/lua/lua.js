/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
define(["require", "exports"], function (require, exports) {
	'use strict';
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.conf = {
		comments: {
			lineComment: '--',
			blockComment: ['--[[', ']]'],
		},
		brackets: [
			['{', '}'],
			['[', ']'],
			['(', ')'],
		],
		autoClosingPairs: [
			{ open: '{', close: '}' },
			{ open: '[', close: ']' },
			{ open: '(', close: ')' },
			{ open: '"', close: '"' },
			{ open: "'", close: "'" },
			{ open: '`', close: '`' },
		],
		surroundingPairs: [
			{ open: '{', close: '}' },
			{ open: '[', close: ']' },
			{ open: '(', close: ')' },
			{ open: '"', close: '"' },
			{ open: "'", close: "'" },
			{ open: '`', close: '`' },
		],
		folding: {
			markers: {
				start: new RegExp("^\\s*--\\s*(?:(?:#?region\\b)|(?:<editor-fold\\b))"),
				end: new RegExp("^\\s*--\\s*(?:(?:#?endregion\\b)|(?:</editor-fold>))")
			}
		},
	};

	exports.language = {
		defaultToken: '',
		tokenPostfix: '.luau',

		keywords: [
			'and', 'break', 'continue', 'do', 'else', 'elseif',
			'end', 'false', 'for', 'function', 'if', 'in',
			'local', 'nil', 'not', 'or', 'repeat', 'return',
			'then', 'true', 'until', 'while',

			'export', 'type', 'typeof', 'declare',
		],

		brackets: [
			{ token: 'delimiter.bracket', open: '{', close: '}' },
			{ token: 'delimiter.array', open: '[', close: ']' },
			{ token: 'delimiter.parenthesis', open: '(', close: ')' }
		],

		globals: [
			'print', 'warn', 'error', 'require', 'game', 'workspace', 'script',
			'assert', 'pcall', 'xpcall', 'typeof', 'type', 'task', 'table', 'math',
			'string', 'os', 'utf8', 'bit32', 'coroutine',
			'spawn', 'delay', 'wait', 'tick', 'time', 'collectgarbage',
			'Instance', 'Vector3', 'CFrame', 'Color3', 'Enum', '_G',
		],

		types: [
			'number', 'string', 'boolean', 'nil', 'any', 'unknown',
			'thread', 'userdata', 'table', 'function', 'never',

			'Axes', 'BrickColor', 'CatalogSearchParams', 'CFrame', 'Color3', 'ColorSequence',
			'ColorSequenceKeypoint', 'DateTime', 'DockWidgetPluginGuiInfo', 'Faces', 'Instance',
			'NumberRange', 'NumberSequence', 'NumberSequenceKeypoint', 'PathWaypoint',
			'PhysicalProperties', 'Random', 'Ray', 'RaycastParams', 'RaycastResult', 'Rect',
			'Region3', 'Region3int16', 'TweenInfo', 'UDim', 'UDim2', 'Vector2', 'Vector2int16',
			'Vector3', 'Vector3int16',
		],

		operators: [
			'+', '-', '*', '/', '%', '^', '#', '..',
			'==', '~=', '<=', '>=', '<', '>', 'or', 'and', 'not',
			'=', '+=', '-=', '*=', '/=', '%=', '^=', '..=',
		],

		symbols: /[=><!~?:&|+\-*\/\^%]+/,
		escapes: /\\(?:[abfnrtv\\"'`]|x[0-9A-Fa-f]{1,4})/,

		tokenizer: {
			root: [
				[/[a-zA-Z_]\w*/, {
					cases: {
						'@keywords': { token: 'keyword.$0' },
						'@globals': { token: 'global' },
						'@types': { token: 'type' },
						'@default': 'identifier'
					}
				}],

				{ include: '@whitespace' },

				[/(,)(\s*)([a-zA-Z_]\w*)(\s*)(:)(?!:)/, ['delimiter', '', 'key', '', 'delimiter']],
				[/({)(\s*)([a-zA-Z_]\w*)(\s*)(:)(?!:)/, ['@brackets', '', 'key', '', 'delimiter']],

				[/[{}()\[\]]/, '@brackets'],

				[/@symbols/, {
					cases: {
						'@operators': 'delimiter',
						'@default': ''
					}
				}],

				[/\d*\.\d+([eE][\-+]?\d+)?/, 'number.float'],
				[/0[xX][0-9a-fA-F_]*[0-9a-fA-F]/, 'number.hex'],
				[/\d+/, 'number'],

				[/[;,.]/, 'delimiter'],

				[/"([^"\\]|\\.)*$/, 'string.invalid'],
				[/'([^'\\]|\\.)*$/, 'string.invalid'],
				[/`([^`\\]|\\.)*$/, 'string.invalid'],
				[/"/, 'string', '@string."'],
				[/'/, 'string', '@string.\''],
				[/`/, 'string', '@string.`'],
			],

			whitespace: [
				[/[ \t\r\n]+/, ''],
				[/--\[([=]*)\[/, 'comment', '@comment.$1'],
				[/--[tT][oO][-]?[dD][oO].*$/, 'comment.todo'],
				[/--.*$/, 'comment'],
			],

			comment: [
				[/[^\]]+/, 'comment'],
				[/\]([=]*)\]/, {
					cases: {
						'$1==$S2': { token: 'comment', next: '@pop' },
						'@default': 'comment'
					}
				}],
				[/./, 'comment']
			],

			string: [
				[/[^\\"'`]+/, 'string'],
				[/@escapes/, 'string.escape'],
				[/\\./, 'string.escape.invalid'],
				[/["'`]/, {
					cases: {
						'$#==$S2': { token: 'string', next: '@pop' },
						'@default': 'string'
					}
				}]
			],
		},
	};
});
