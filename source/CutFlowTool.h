#ifndef CUTFLOWTOOL_H_1234 
#define CUTFLOWTOOL_H_1234


#include <string>
#include <vector>
#include <ostream>
#include <map>
#include <math.h> 

class CutFlowTool {
  public:
    class CutCount {
      public:
        CutCount(): 
          num(0.), wnum(0.), sumw2(0.), err(0.) {}
        // the counter plus one!
        void count(double);
        void finalize() { err = sqrt(sumw2); }

        double num;
        double wnum;
        double sumw2;
        double err;
    };

    class Flow {
      public:
        // should not be called, but must have it
        // for default constructor for map[]
        Flow(): title("NOT SET, please debug"), ncut(0), prev_incl(false), last_noninc(0) {}
        Flow(std::string title): title(title),  ncut(0), prev_incl(false), last_noninc(0) {}
        Flow& regCut(std::string name, std::string title = "", bool inc = false);
        // Flow& regCut(std::string name, bool inc);
        Flow& refresh() {
          m_prev_noninc.back() = 0;
          return *this;
        }
        void pass(std::string& cut, double w);
        // pass last non-inc cut
        bool isPass() {
          return m_vec_pass[last_noninc];
        }
        // pass any cut
        bool isPass(std::string& cut) { 
          return m_vec_pass[m_map_cut[cut].first];
        }
        // this CutCount
        CutCount& thisCC(std::string& cut) {
          return m_map_cut[cut].second;
        }
        // index of this CutCount
        uint32_t thisCCi(std::string& cut) {
          return m_map_cut[cut].first;
        }
        std::string title;
        uint32_t ncut;
        bool prev_incl;
        uint32_t last_noninc;
        // vector of cut names
        std::vector<std::string> m_vec_cut;
        // the previous non inclusive cut(including this one) 
        std::vector<uint32_t>    m_prev_noninc;
        std::vector<bool>        m_vec_pass;
        // cut names : <index, CutCount>
        std::map<std::string, std::pair<uint32_t, CutCount>> m_map_cut;
        std::map<std::string, std::string> m_map_title;
    };

    CutFlowTool(std::string name) : m_name(name) {}
    // forward declaration
    // register a name(identifier)
    // title is the more beautiful indicator shown in printout..
    Flow& regFlow(std::string name, std::string title);
    // the behavior: for each flow, 
    // at least register one cut and pass it, call it "All"
    // inclusive cut means it's a cut that will follow the 
    // flow of the last non-inclusive cut, usually used for channels
    Flow& regCut(std::string flowName, std::string cutName, std::string cutTitle = "", bool inclusive = false);
    // Flow& regCut(std::string flowName, std::string cutName, bool inclusive);
    void pass(std::string flowName, std::string cutName, double w = 1.);
    // cutName1 is also the name of a flow 
    // usually used with each channel
    void pass(std::string flowName, std::string cutName1, 
        std::string cutName2, double w = 1.){
      pass(flowName, cutName1, w);
      pass(cutName1, cutName2, w);
    }
    bool isPass(std::string flowName, std::string cutName) { 
      return m_map_flow[flowName].isPass(cutName);
    }
    void print(std::ostream&);

  private:
    std::string m_name;
    std::vector<std::string> m_vec_flow;
    std::map<std::string, Flow> m_map_flow;
};
#endif
