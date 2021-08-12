#include "CutFlowTool.h"
#include <iostream>
#include <iomanip>

// user interface:
CutFlowTool::Flow& CutFlowTool::regFlow(std::string name, 
    std::string title) {
  if (m_map_flow.find(name) != m_map_flow.end()) {
    std::cerr <<  "The Flow [" << name << "] already exist" << std::endl;
    exit(1);
  }
  m_vec_flow.push_back(name);
  m_map_flow.emplace(name, title);
  return m_map_flow[name];
}

// do not do safety check here
CutFlowTool::Flow& CutFlowTool::regCut(std::string flowName, 
    std::string cutName,
    std::string cutTitle,
    bool inclusive) {
  m_map_flow[flowName].regCut(cutName, cutTitle, inclusive);
  return m_map_flow[flowName];
}

// CutFlowTool::Flow& CutFlowTool::regCut(std::string flowName, 
    // std::string cutName,
    // bool inclusive) {
  // return regCut(flowName, cutName, cutName, inclusive);
// }

void CutFlowTool::pass(
    std::string flowName, 
    std::string cutName, 
    double w) {
  m_map_flow[flowName].pass(cutName, w);
}


void CutFlowTool::print(std::ostream& s){
  s << "======================================="
    "=========================" << std::endl;
  s << "The START of my fancy cut flows: " 
    << m_name << std::endl;
  s << "======================================="
      "=========================" << std::endl;

  for (const auto & flown: m_vec_flow) {
    auto & flow = m_map_flow[flown];
    // s << std::endl << "---------------------------------------"
      // "-------------------------" << std::endl;
    s << flow.title << std::endl;
    s << "---------------------------------------" 
      "-------------------------" << std::endl;
    std::string firstCN = "";
    std::string prevCN = "";
    for (const auto & cutn: flow.m_vec_cut) {
      auto & cut = flow.m_map_cut[cutn].second;
      auto index = flow.m_map_cut[cutn].first;
      cut.finalize();

      s << std::setprecision(10);
      s << flow.m_map_title[cutn] << ": " <<  cut.num 
        << " (" << cut.wnum 
        << " +/- "  <<  cut.err << ")" ;
      
      s << std::setprecision(4);
      if (firstCN == "") {
        firstCN = cutn;
      } else {
        auto & cutFirst = flow.m_map_cut[firstCN].second;
        //auto & cutPrev  = flow.m_map_cut[prevCN].second;
        auto & cutPrev  = flow.m_map_cut[flow.m_vec_cut[flow.m_prev_noninc[index]]].second;
        s << " [Unwgt(Wgt) Eff abs/rel: "  << cut.num / (cutFirst.num != 0 ? cutFirst.num: 1) <<  "/" <<  
          cut.num / (cutPrev.num != 0 ? cutPrev.num: 1);
        s << " ("  << cut.wnum / (cutFirst.wnum != 0 ? cutFirst.wnum: 1) <<  "/" <<  
          cut.wnum / (cutPrev.wnum != 0 ? cutPrev.wnum: 1)
          << ")] ";
      }

      s << std::setprecision(6);
      //prevCN = cutn;
      s << std::endl;
    }
    s << "---------------------------------------" 
      "-------------------------" << std::endl;
  }

  s << "======================================="
      "=========================" << std::endl;
}


CutFlowTool::Flow& CutFlowTool::Flow::regCut(
    std::string name, std::string title, bool inc) {
  if (m_map_cut.find(name) != m_map_cut.end()) {
    std::cerr <<  "The Cut [" << name << "] already exist for "
      "Flow [" << title << "]" << std::endl;
    exit(1);
  }

  if (prev_incl)
    // follows previous inclusive cut, find hist non-inclusive
    m_prev_noninc.push_back( m_prev_noninc.back() );
  else 
    // look at last cut directly
    m_prev_noninc.push_back( ncut - 1 );


  if (inc) {
    prev_incl = true;
  } else {
    last_noninc = ncut;
    prev_incl = false;
  }
  // m_map_cut.emplace(std::make_pair(name, 
        // std::make_pair(ncut, CutCount())));
  m_map_cut.emplace(name, 
        std::make_pair(ncut, CutCount()));
  if (title == "") title = name;
  m_map_title[name] = title;
  m_vec_cut.push_back(name);
  m_vec_pass.push_back(false);
  ncut += 1;

  return *this;
}

// CutFlowTool::Flow& CutFlowTool::Flow::regCut(
    // std::string name, bool inc) {
  // std::cerr << name << "debug" << inc << std::endl;
  // return regCut(name, name, inc);
// }

void CutFlowTool::Flow::pass(std::string& cut, double w) {
  auto index = m_map_cut[cut].first;
  if (index == 0) {
    thisCC(cut).count(w);
    // reinitialize the list
    std::fill(m_vec_pass.begin() + 1, m_vec_pass.end(), false);
    m_vec_pass[0] = true;
  } else if (m_vec_pass[m_prev_noninc[index]] ) {
    thisCC(cut).count(w);
    m_vec_pass[m_map_cut[cut].first] = true;
  }
}

void CutFlowTool::CutCount::count(double w) {
  num   += 1;
  wnum  += w;
  sumw2 += w * w;
}
