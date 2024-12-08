use std::collections::HashMap;
use std::fmt;
use std::num::ParseIntError;
use std::str::FromStr;

use utils;

#[derive(Debug, Clone)]
struct Rule(u32, u32);
struct RuleSet {
    data: Vec<Rule>,
    // map: HashMap<u32, Vec<&'a Rule>>,
}
struct UpdatePages(Vec<u32>);
struct UpdateSet(Vec<UpdatePages>);

impl FromStr for Rule {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (p, f) = s.split_once("|").ok_or(fmt::Error)?;
        let p = p.parse().map_err(|_| fmt::Error)?;
        let f = f.parse().map_err(|_| fmt::Error)?;
        Ok(Self(p, f))
    }
}

type RuleMap<'a> = HashMap<u32, Vec<&'a Rule>>;

impl RuleSet {
    fn rule_map(&self) -> RuleMap {
        let mut map = HashMap::new();
        let mut update_map = |key, rule| {
            let e = map.entry(key).or_insert(Vec::new());
            e.push(rule)
        };
        for rule in &self.data {
            update_map(rule.0, rule)
        }
        map
    }
}

impl FromStr for UpdatePages {
    type Err = fmt::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self(
            s.split(",")
                .map(|v| v.parse::<u32>())
                .collect::<Result<Vec<u32>, ParseIntError>>()
                .map_err(|_| fmt::Error)?,
        ))
    }
}

impl UpdatePages {
    fn is_valid(&self, rules: &RuleSet, rule_map: Option<&RuleMap>) -> bool {
        let rule_map = match rule_map {
            Some(rm) => rm,
            None => &rules.rule_map(),
        };
        for (i, p) in self.0.iter().enumerate() {
            let rs = &rule_map.get(p);
            let Some(rs) = rs else {
                continue;
            };
            for r in *rs {
                assert!(r.0 == *p || r.1 == *p);
                // if i == 1 && *p == 97 {
                //     println!();
                //     println!("{:?}", r);
                //     println!("{:?}", self.0);
                //     println!("{:?}", &self.0[..i]);
                // }
                if r.0 == *p && self.0[..i].contains(&r.1) {
                    return false;
                } else if r.1 == *p && self.0[i + 1..].contains(&r.0) {
                    return false;
                }
            }
        }
        true
    }

    fn middle_number(&self) -> u32 {
        let len = self.0.len();
        assert_eq!(len % 2, 1);
        let index = (len - 1) / 2;
        self.0[index]
    }
}

impl UpdateSet {
    fn valid_updates(&self, rules: &RuleSet) -> Vec<bool> {
        self.0
            .iter()
            .map(|u| u.is_valid(rules, Some(&rules.rule_map())))
            .collect()
    }

    fn checksum(&self, rules: &RuleSet) -> u32 {
        let rm = Some(rules.rule_map());
        self.0
            .iter()
            .filter(|p| p.is_valid(rules, rm.as_ref()))
            .map(|p| p.middle_number())
            .sum()
    }
}

fn parse_input(input: Vec<String>) -> (RuleSet, UpdateSet) {
    let mut parts = input.split(|s| s == "");
    let rule_strs = parts.next().unwrap();
    let update_strs = parts.next().unwrap();
    assert!(parts.next().is_none());

    let rules = RuleSet {
        data: rule_strs
            .iter()
            .map(|s| Rule::from_str(s).unwrap())
            .collect(),
    };

    let updates = UpdateSet(
        update_strs
            .iter()
            .map(|s| UpdatePages::from_str(s).unwrap())
            .collect(),
    );

    (rules, updates)
}

fn main() {
    let input = utils::input_lines(5);
    let (rules, updates) = parse_input(input);
    let part_1_answer = updates.checksum(&rules);
    println!("Day 5, Part 1 answer: {}", part_1_answer);
}

#[cfg(test)]
mod test;
