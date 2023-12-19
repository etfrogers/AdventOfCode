package digits

import (
	"fmt"
	"regexp"
)

var digitList = []string{
	"one",
	"two",
	"three",
	"four",
	"five",
	"six",
	"seven",
	"eight",
	"nine",
}

var DIGIT_MAPPING = map[string]int{}
var DigitWordRegexps []*regexp.Regexp

func init() {
	for i, key := range digitList {
		DIGIT_MAPPING[key] = i + 1
		DigitWordRegexps = append(DigitWordRegexps, regexp.MustCompile(key))
	}
	for i := 1; i < 10; i++ {
		DIGIT_MAPPING[fmt.Sprint(i)] = i
	}

	// keys := []string{}
	// for _, k := range digitList {
	// 	keys = append(keys, "("+k+")")
	// }
	// re_str := strings.Join(keys, "|")
	// re_str += "|(\\d)"
	// digit_word_regexp = regexp.MustCompile(re_str)
}
