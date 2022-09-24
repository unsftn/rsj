import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MenuItem, MessageService, PrimeNGConfig } from 'primeng/api';
import { Container, Engine } from "tsparticles-engine";
// import { loadFull } from "tsparticles";
import { loadConfettiPreset } from 'tsparticles-preset-confetti';
import { StatsService } from '../../services/reci/stats.service';
import { SearchService } from '../../services/search/search.service';

@Component({
  selector: 'toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss']
})
export class ToolbarComponent implements OnInit {

  workflowItems: MenuItem[];
  @Input() title = '';
  @Input() saveAvailable: boolean = true;
  @Output() saveClicked = new EventEmitter();
  mode: string;

  constructor(
    private route: ActivatedRoute,
    private primengConfig: PrimeNGConfig,
    private messageService: MessageService,
    private statsService: StatsService,
    private searchService: SearchService,
  ) { }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.route.data.subscribe((data) => {
      this.mode = data.mode;
    });
  }

  undoAvailable(): boolean {
    return true;
  }

  redoAvailable(): boolean {
    return true;
  }

  workflowDisabled(): boolean {
    return false;
  }

  undo(): void {
    this.notImplemented();
  }

  redo(): void {
    this.notImplemented();
  }

  preview(): void {
    this.notImplemented();
  }

  save(): void {
    this.saveClicked.emit();
    this.searchService.clear();
    setTimeout(() => {
      this.statsService.getBrojMojihReci().subscribe({
        next: (data) => { 
          if (this.mode === 'add' && data % 10 === 0) {
            this.container.start(); 
            this.container.play();
            setTimeout(() => { this.container.stop(); }, 5000);
            this.messageService.add({
              severity: 'info', summary: 'Честитка', life: 5000, detail: `Унели сте укупно ${data} речи!`
            });
          }
        },
        error: (error) => { console.log(error); }
      });
    }, 500);
  }

  delete(): void {
    this.notImplemented();
  }

  notImplemented(): void {
    this.messageService.add({
      severity: 'error',
      summary: 'Грешка',
      life: 5000,
      detail: `Још не ради`,
    });
  }

  id = 'tsparticles';

  particlesOptions = {
    // preset: "confetti",
    "fullScreen": {
      "zIndex": 1
    },
    "particles": {
      "number": {
        "value": 0
      },
      "color": {
        "value": ["#1E00FF", "#FF0061", "#E1FF00", "#00FF9E"]
      },
      "shape": {
        "type": [
          "circle",
          "square",
          "triangle"
        ],
        "options": {}
      },
      "opacity": {
        "value": 1,
        "animation": {
          "enable": true,
          "minimumValue": 0,
          "speed": 2,
          "startValue": "max",
          "destroy": "min"
        }
      },
      "size": {
        "value": 6,
        "random": {
          "enable": true,
          "minimumValue": 2
        }
      },
      "links": {
        "enable": false
      },
      "life": {
        "duration": {
          "sync": true,
          "value": 5
        },
        "count": 1
      },
      "move": {
        "enable": true,
        "gravity": {
          "enable": true,
          "acceleration": 10
        },
        "speed": {
          "min": 10,
          "max": 20
        },
        "decay": 0.1,
        "direction": "none",
        "straight": false,
        "outModes": {
          "default": "destroy",
          "top": "none"
        }
      },
      "rotate": {
        "value": {
          "min": 0,
          "max": 360
        },
        "direction": "random",
        "move": true,
        "animation": {
          "enable": true,
          "speed": 60
        }
      },
      "tilt": {
        "direction": "random",
        "enable": true,
        "move": true,
        "value": {
          "min": 0,
          "max": 360
        },
        "animation": {
          "enable": true,
          "speed": 60
        }
      },
      "roll": {
        "darken": {
          "enable": true,
          "value": 25
        },
        "enable": true,
        "speed": {
          "min": 15,
          "max": 25
        }
      },
      "wobble": {
        "distance": 30,
        "enable": true,
        "move": true,
        "speed": {
          "min": -15,
          "max": 15
        }
      }
    },
    "emitters": {
      "life": {
        "count": 0,
        "duration": 0.1,
        "delay": 0.4
      },
      "rate": {
        "delay": 0.1,
        "quantity": 150
      },
      "size": {
        "width": 0,
        "height": 0
      }
    }
  };

  container: Container;
  engine: Engine;

  particlesLoaded(container: Container): void {
    this.container = container;
    this.container.stop();
  }

  async particlesInit(engine: Engine): Promise<void> {
    this.engine = engine;
    // await loadFull(engine);
    await loadConfettiPreset(engine);
  }
}
