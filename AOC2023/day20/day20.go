package main

import (
	"fmt"
	"regexp"
	"strings"
	"utils"
	"utils/iter"
	"utils/queue"
)

type Machine struct {
	nodes         map[string]Processor
	nLow, nHigh   int
	flipFlopNames []string
}

type Inputs map[string]Pulse

type Processor interface {
	ProcessSignal(from string, pulse Pulse) []Signal
	setOutputs([]string)
	getOutputs() []string
	setName(string)
}

type Module struct {
	name    string
	outputs []string
}

type Conjunction struct {
	Module
	inputs Inputs
}

type FlipFlop struct {
	Module
	isOn bool
}

type Broadcaster struct {
	Module
}

type Signal struct {
	from, to string
	pulse    Pulse
}

type ModuleType int
type Pulse int

const (
	High Pulse = iota
	Low
)

var moduleRe regexp.Regexp = *regexp.MustCompile(`((broadcaster)|([%&])([a-z]+)) -> ([a-z ,]+)`)

func BuildModule(line string) (string, Processor) {
	tokens := moduleRe.FindStringSubmatch(line)
	var name string
	var m Processor
	if tokens[1] == "broadcaster" {
		m = &Broadcaster{}
		name = "broadcaster"
	} else {
		switch tokens[3] {
		case "&":
			m = &Conjunction{inputs: make(Inputs, 0)}

		case "%":
			m = &FlipFlop{isOn: false}
		default:
			panic("unknown type")
		}
		name = tokens[4]
	}
	outputStr := tokens[5]
	m.setOutputs(strings.Split(outputStr, ", "))
	m.setName(name)

	return name, m
}

func BuildMachine(lines []string) Machine {
	m := Machine{nodes: make(map[string]Processor, len(lines)), nLow: 0, nHigh: 0}
	for _, line := range lines {
		name, mod := BuildModule(line)
		m.nodes[name] = mod
	}

	for name, node := range m.nodes {
		for _, link := range node.getOutputs() {
			reciver := m.nodes[link]
			if r, ok := reciver.(*Conjunction); ok {
				r.inputs[name] = Low
			}
		}
		if _, ok := node.(*FlipFlop); ok {
			m.flipFlopNames = append(m.flipFlopNames, name)
		}
	}
	return m
}

func (m *Machine) Run(n int) {
	for i := range n {
		fmt.Println(i)
		m.RunCycle()
	}
}

func (m *Machine) RunCycle() {
	pulses := queue.New[Signal]()
	pulses.Push(Signal{to: "broadcaster", from: "button", pulse: Low})
	for pulses.Len() > 0 {
		sig := pulses.Pop()
		switch sig.pulse {
		case Low:
			m.nLow++
		case High:
			m.nHigh++
		default:
			panic("unexpected value")
		}
		reciever, ok := m.nodes[sig.to]
		if !ok {
			// receiver module not present: signal can be sent, but nothing should be processed
			continue
		}
		newPulses := reciever.ProcessSignal(sig.from, sig.pulse)
		pulses.Push(newPulses...)
	}
}

func (m *Module) setOutputs(os []string) {
	m.outputs = os
}

func (m *Module) setName(n string) {
	m.name = n
}

func (m *Module) getOutputs() []string {
	return m.outputs
}

func (m *Module) pulsesForOutputs(pulse Pulse) []Signal {
	return utils.Map(m.outputs, func(name string) Signal { return Signal{from: m.name, to: name, pulse: pulse} })
}

func (m *Broadcaster) ProcessSignal(from string, pulse Pulse) []Signal {
	if from != "button" || pulse != Low {
		panic("unexpected state")
	}
	return m.pulsesForOutputs(Low)
}

func (m *FlipFlop) ProcessSignal(from string, pulse Pulse) []Signal {
	if pulse == High {
		return []Signal{}
	} else {
		// Low
		var outPulse Pulse
		if m.isOn {
			m.isOn = false
			outPulse = Low

		} else {
			m.isOn = true
			outPulse = High
		}
		return m.pulsesForOutputs(outPulse)
	}
}

func (m *Conjunction) ProcessSignal(from string, pulse Pulse) []Signal {
	m.inputs[from] = pulse
	var outPulse Pulse
	if iter.All(iter.Map(func(p Pulse) bool { return p == High }, iter.Values(m.inputs))) {
		outPulse = Low
	} else {
		outPulse = High
	}
	return m.pulsesForOutputs(outPulse)
}

func (m *Machine) Checksum() int {
	return m.nHigh * m.nLow
}

func main() {
	lines := utils.ReadInput()
	m := BuildMachine(lines)
	m.Run(1000)
	part1Answer := m.Checksum()
	fmt.Printf("Day 20, Part 1 answer: %d\n", part1Answer)
}
